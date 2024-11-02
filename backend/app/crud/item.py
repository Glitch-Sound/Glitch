from sqlalchemy import select, update, distinct, and_, or_, func, case, text, literal
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import func

import sys
sys.path.append('~/app')

from crud.common import generate_bigrams, getWeekAgoDate, getCurrentDatetime, ItemType, ItemState, ExtractType, TaskType, RiskType
from crud.summary import createSummaryItem, createSummaryUser

from schema import item as schema_item
from model.item import Item
from model.tree import Tree
from model.project import Project
from model.event import Event
from model.feature import Feature
from model.story import Story
from model.task import Task
from model.bug import Bug
from model.user import User

import jpholiday
import datetime


class ItemParam():
    def __init__(self, type_extract: ExtractType, id_project: int, rid_users: int = None, rid_items: int = None, search: str  = None):
        self.type_extract = type_extract
        self.id_project   = id_project
        self.rid_users    = rid_users if rid_users is not None else 0
        self.rid_items    = rid_items if rid_items is not None else 0
        self.search       = search    if search    is not None else ''


class ItemUpdateCommon():
    def __init__(self, rid: int, state: int, rid_users: int, rid_users_review: int, title: str, detail: str, result: str):
        self.rid              = rid
        self.state            = state
        self.rid_users        = rid_users
        self.rid_users_review = rid_users_review
        self.title            = title
        self.detail           = detail
        self.result           = result


def _createTree(db: Session, type_create: ItemType, rid_parent: int, rid: int):
    try:
        trees = db.query(
            Tree.rid_ancestor
        )\
        .filter(Tree.rid_descendant == rid_parent)\
        .order_by(Tree.rid_ancestor).all()

        if not trees:
            raise

        list_rid_ancestor = [r[0] for r in trees]
        list_rid_ancestor.append(rid)

        for index, rid_ancestor in enumerate(list_rid_ancestor):
            type = index + 1
            if rid_ancestor == rid:
                type = type_create.value

            tree = Tree(
                rid_ancestor=rid_ancestor,
                rid_descendant=rid,
                type=type
            )
            db.add(tree)

    except Exception as e:
        raise e


def _createNextRID(db: Session):
    try:
        next_rid = db.query(
            func.coalesce(func.max(Item.rid), 0) + 1
        )\
        .scalar()

        return next_rid

    except Exception as e:
        raise e


def _createSortPathProject(id_project: int):
    return str(id_project).zfill(4) + "00000000000000000000000000000"


def _createSortPathEvent(db: Session, target:schema_item.EventCreate):
    try:
        next_rid  = _createNextRID(db)
        path_sort = str(target.id_project).zfill(4) + target.event_datetime_end.replace('-', '') + str(next_rid).zfill(4) + '00000000000000000'

        return path_sort

    except Exception as e:
        raise e


def _createSortPathFeature(db: Session, target:schema_item.FeatureCreate):
    try:
        path_sort_event = db.query(
            Item.path_sort
        )\
        .filter(
            Item.rid == target.rid_items
        )\
        .one()[0]

        next_rid  = _createNextRID(db)

        path_sort = path_sort_event[:16] + str(next_rid).zfill(4) + '0000000000000'
        return path_sort

    except Exception as e:
        raise e


def _createSortPathStory(db: Session, target:schema_item.StoryCreate):
    try:
        path_sort_feature = db.query(
            Item.path_sort
        )\
        .filter(
            Item.rid == target.rid_items
        )\
        .one()[0]

        next_rid  = _createNextRID(db)

        path_sort = path_sort_feature[:20] + target.story_datetime_end.replace('-', '') + str(next_rid).zfill(4) + '0'
        return path_sort

    except Exception as e:
        raise e


def _createSortPathTask(db: Session, target:schema_item.TaskCreate):
    try:
        path_sort_story = db.query(
            Item.path_sort
        )\
        .filter(
            Item.rid == target.rid_items
        )\
        .one()[0]

        path_sort = path_sort_story[:32] + str(ItemType.TASK.value)
        return path_sort

    except Exception as e:
        raise e


def _createSortPathBug(db: Session, target:schema_item.BugCreate):
    try:
        path_sort_story = db.query(
            Item.path_sort
        )\
        .filter(
            Item.rid == target.rid_items
        )\
        .one()[0]

        path_sort = path_sort_story[:32] + str(ItemType.BUG.value)
        return path_sort

    except Exception as e:
        raise e


def _updateSortPathEvent(db: Session, rid: int, event_datetime_end: str):
    try:
        t1 = aliased(Tree)
        t2 = aliased(Item)

        subquery = (
            db.query(
                t2.rid
            )\
            .join(t1, t1.rid_descendant == t2.rid)\
            .filter(t1.rid_ancestor == rid)\
            .subquery()
        )

        update_query = (
            update(Item)
            .where(Item.rid.in_(subquery))
            .values(
                path_sort=(
                    func.substr(Item.path_sort, 1, 4) +
                    literal(event_datetime_end.replace('-', '')) +
                    func.substr(Item.path_sort, 13)
                )
            )
        )
        db.execute(update_query)

    except Exception as e:
        raise e


def _updateSortPathStory(db: Session, rid: int, story_datetime_end: str):
    try:
        t1 = aliased(Tree)
        t2 = aliased(Item)

        subquery = (
            db.query(
                t2.rid
            )\
            .join(t1, t1.rid_descendant == t2.rid)\
            .filter(t1.rid_ancestor == rid)\
            .subquery()
        )

        update_query = (
            update(Item)
            .where(Item.rid.in_(subquery))
            .values(
                path_sort=(
                    func.substr(Item.path_sort, 1, 20) +
                    literal(story_datetime_end.replace('-', '')) +
                    func.substr(Item.path_sort, 29)
                )
            )
        )
        db.execute(update_query)

    except Exception as e:
        raise e


def _getDateLimit(db: Session, rid: int):
    try:
        story = db.query(
            Story.datetime_end
        )\
        .join(Tree, Story.rid_items == Tree.rid_ancestor)\
        .where(
            Tree.rid_descendant == rid,
            Tree.type == ItemType.STORY.value
        )\
        .one()

        return story.datetime_end

    except Exception as e:
        raise e


def _getTargetItem(db: Session, rid_item: int):
    try:
        query = db.query(
            Item.rid,
            Task.type.label('task_type'),
            Task.workload.label('task_workload'),
            Task.number_total.label('task_number_total'),
            Bug.workload.label('bug_workload'))\
        .outerjoin(Task, Task.rid_items == Item.rid)\
        .outerjoin(Bug, Bug.rid_items == Item.rid)\
        .filter(Item.rid == rid_item)\

        result = query.one()
        return result

    except Exception as e:
        raise e


def _getRisk(db: Session, rid_item: int):
    try:
        datetime_limit   = _getDateLimit(db, rid_item)
        datetime_current = getCurrentDatetime()

        date_format  = "%Y-%m-%d"
        date_limit   = datetime.datetime.strptime(datetime_limit.split(' ')[0], date_format).date()
        date_current = datetime.datetime.strptime(datetime_current.split(' ')[0], date_format).date()

        day_active = 0
        delta      = datetime.timedelta(days=1)
        date       = date_current

        while date <= date_limit:
            if date.weekday() < 5 and not jpholiday.is_holiday(date):
                day_active += 1
            date += delta

        item = _getTargetItem(db, rid_item)

        workload = 0
        if item.task_workload is not None:
            workload = item.task_workload
        else:
            workload = item.bug_workload

        if (day_active - workload / 7) <= 0:
            return RiskType.OVER

        if (day_active - workload / 7) <= 2:
            return RiskType.LIMIT

        return RiskType.NONE

    except Exception as e:
        raise e


def _setRisk(db: Session, rid_item: int):
    try:
        risk = _getRisk(db, rid_item)

        target_item = db.query(
            Item
        )\
        .filter(Item.rid == rid_item)

        target_item.update({
            Item.risk: risk.value
        })

    except Exception as e:
        raise e


def _updateItem(db: Session, target: ItemUpdateCommon):
    try:
        datetime_current = getCurrentDatetime()

        item = db.query(
            Item
        )\
        .filter(Item.rid == target.rid)

        if target.state != ItemState.COMPLETE.value:
            item.update({
                Item.state: target.state,
                Item.rid_users: target.rid_users,
                Item.rid_users_review: target.rid_users_review,
                Item.title:  target.title,
                Item.detail: target.detail,
                Item.result: target.result,
                Item.datetime_update: datetime_current
            })
        else:
            item.update({
                Item.state: target.state,
                Item.risk: 0,
                Item.rid_users: target.rid_users,
                Item.rid_users_review: target.rid_users_review,
                Item.title: target.title,
                Item.detail: target.detail,
                Item.result: target.result,
                Item.datetime_update: datetime_current
            })

        item_updated = item.first()
        return item_updated

    except Exception as e:
        raise e


def _deleteItem(db: Session, rid: int):
    try:
        datetime_current = getCurrentDatetime()

        db.begin()
        item = db.query(
            Item
        )\
        .filter(Item.rid == rid)

        item.update({
            Item.is_deleted: 1,
            Item.datetime_update: datetime_current
        })
        db.commit()

    except Exception as e:
        db.rollback()
        raise e


def _extructItem(db: Session, params: ItemParam):
    try:
        cte_extruct = None
        match params.type_extract:
            case ExtractType.ALL.value:
                cte_extruct = db.query(
                    Tree.rid_descendant.label('rid')
                )\
                .filter(Tree.rid_ancestor == params.id_project)

            case ExtractType.INCOMPLETE.value:
                subquery_target = (
                    select(Item.rid)
                    .where(Item.state != ItemState.COMPLETE.value)
                ).subquery()

                cte_extruct = db.query(
                    distinct(Tree.rid_descendant).label('rid')
                )\
                .where(Tree.rid_descendant.in_(select(subquery_target)))

            case ExtractType.HIGH_RISK.value:
                subquery_target = (
                    select(Item.rid)
                    .where(
                        Item.state != ItemState.COMPLETE.value,
                        Item.risk != 0
                    )
                ).subquery()

                cte_extruct = db.query(
                    distinct(Tree.rid_ancestor).label('rid')
                )\
                .where(Tree.rid_descendant.in_(select(subquery_target)))

            case ExtractType.ALERT.value:
                subquery_target = (
                    select(Item.rid)
                    .where(Item.state == ItemState.ALERT.value)
                ).subquery()

                cte_extruct = db.query(
                    distinct(Tree.rid_ancestor).label('rid')

                )\
                .where(Tree.rid_descendant.in_(select(subquery_target)))

            case ExtractType.ASSIGNMENT.value:
                subquery_target = (
                    select(Item.rid)
                    .where(Item.rid_users == params.rid_users)
                ).subquery()

                cte_extruct = db.query(
                    distinct(Tree.rid_ancestor).label('rid')
                )\
                .where(Tree.rid_descendant.in_(select(subquery_target)))

            case ExtractType.RELATION.value:
                cte_extruct_ancestor = db.query(
                    Tree.rid_ancestor.label('rid')
                )\
                .filter(Tree.rid_descendant == params.rid_items)

                cte_extruct_descendant = db.query(
                    Tree.rid_descendant.label('rid')
                ).filter(Tree.rid_ancestor == params.rid_items)

                cte_extruct = cte_extruct_ancestor.union(cte_extruct_descendant)

            case ExtractType.SEARCH.value:
                search_bigrams = generate_bigrams(params.search)
                fts_query_bigrams = text("""
                    SELECT rowid FROM items_fts WHERE items_fts.bigrams MATCH :search_query
                """)

                rids = db.execute(fts_query_bigrams, {'search_query': search_bigrams}).scalars().all()

                matching_rids = set(rids)
                subquery_target = (
                    select(Item.rid)
                    .where(
                        and_(
                            Item.id_project == params.id_project,
                            Item.rid.in_(matching_rids)
                        )
                    )
                ).subquery()

                cte_extruct = db.query(
                    distinct(Tree.rid_ancestor).label('rid')
                ).where(Tree.rid_descendant.in_(select(subquery_target)))

            case ExtractType.ANCESTOR.value:
                cte_extruct = db.query(
                    Tree.rid_ancestor.label('rid')
                )\
                .filter(Tree.rid_descendant == params.rid_items)

            case ExtractType.SUMMARY_USER.value:
                datetime_week_ago = getWeekAgoDate()

                subquery_target = (
                    select(Item.rid)
                    .where(
                        Item.rid_users == params.rid_users,
                        datetime_week_ago <= Item.datetime_update
                    )
                ).subquery()

                cte_extruct = db.query(
                    distinct(Tree.rid_ancestor).label('rid')
                )\
                .where(Tree.rid_descendant.in_(select(subquery_target)))

        return cte_extruct.cte(name='targets')

    except Exception as e:
        raise e


def getItems(db: Session, params: ItemParam):
    try:
        UserAlias1 = aliased(User)
        UserAlias2 = aliased(User)

        cte_extruct = _extructItem(db, params)

        query = db.query(
            Item.rid,
            Item.id_project,
            Item.type,
            Item.state,
            Item.risk,
            Item.priority,
            Item.title,
            Item.detail,
            Item.result,
            Item.datetime_entry,
            Item.datetime_update,
            UserAlias1.rid.label('rid_users'),
            UserAlias1.name.label('name'),
            UserAlias2.rid.label('rid_users_review'),
            UserAlias2.name.label('name_review'),
            Project.datetime_start.label('project_datetime_start'),
            Project.datetime_end.label('project_datetime_end'),
            Event.datetime_end.label('event_datetime_end'),
            Story.datetime_start.label('story_datetime_start'),
            Story.datetime_end.label('story_datetime_end'),
            Task.type.label('task_type'),
            Task.workload.label('task_workload'),
            Task.number_completed.label('task_number_completed'),
            Task.number_total.label('task_number_total'),
            Bug.workload.label('bug_workload'))\
        .select_from(cte_extruct)\
        .join(Item, Item.rid == cte_extruct.c.rid)\
        .outerjoin(UserAlias1,  UserAlias1.rid == Item.rid_users)\
        .outerjoin(UserAlias2,  UserAlias2.rid == Item.rid_users_review)\
        .outerjoin(Project, Project.rid_items == Item.rid)\
        .outerjoin(Event, Event.rid_items == Item.rid)\
        .outerjoin(Feature, Feature.rid_items == Item.rid)\
        .outerjoin(Story, Story.rid_items == Item.rid)\
        .outerjoin(Task, Task.rid_items == Item.rid)\
        .outerjoin(Bug, Bug.rid_items == Item.rid)\
        .where(Item.is_deleted == 0)\
        .order_by(Item.path_sort, Item.priority.desc(), Item.rid)

        result = query.all()
        return result

    except Exception as e:
        raise e


def getItemsNotice(db: Session, id_project):
    try:
        UserAlias1 = aliased(User)
        UserAlias2 = aliased(User)

        cte_extruct_ancestor = db.query(
            Tree.rid_ancestor.label('rid')
        )\
        .join(Item,  Item.rid == Tree.rid_descendant)\
        .join(Story, Item.rid == Story.rid_items)\
        .where(
            Item.id_project == id_project,
            Item.state != ItemState.COMPLETE.value
        )

        cte_extruct_descendant = db.query(
            Tree.rid_descendant.label('rid')
        )\
        .join(Item, Item.rid == Tree.rid_ancestor)\
        .join(Story, Item.rid == Story.rid_items)\
        .where(
            Item.id_project == id_project,
            Item.state != ItemState.COMPLETE.value
        )

        cte_extruct = cte_extruct_ancestor.union(cte_extruct_descendant).cte(name='targets')

        query = db.query(
            Item.rid,
            Item.id_project,
            Item.type,
            Item.state,
            Item.risk,
            Item.priority,
            Item.title,
            Item.detail,
            Item.result,
            Item.datetime_entry,
            Item.datetime_update,
            UserAlias1.rid.label('rid_users'),
            UserAlias1.name.label('name'),
            UserAlias2.rid.label('rid_users_review'),
            UserAlias2.name.label('name_review'),
            Project.datetime_start.label('project_datetime_start'),
            Project.datetime_end.label('project_datetime_end'),
            Event.datetime_end.label('event_datetime_end'),
            Story.datetime_start.label('story_datetime_start'),
            Story.datetime_end.label('story_datetime_end'),
            Task.type.label('task_type'),
            Task.workload.label('task_workload'),
            Task.number_completed.label('task_number_completed'),
            Task.number_total.label('task_number_total'),
            Bug.workload.label('bug_workload'))\
        .select_from(cte_extruct)\
        .join(Item, Item.rid == cte_extruct.c.rid)\
        .outerjoin(UserAlias1,  UserAlias1.rid == Item.rid_users)\
        .outerjoin(UserAlias2,  UserAlias2.rid == Item.rid_users_review)\
        .outerjoin(Project, Project.rid_items == Item.rid)\
        .outerjoin(Event, Event.rid_items == Item.rid)\
        .outerjoin(Feature, Feature.rid_items == Item.rid)\
        .outerjoin(Story, Story.rid_items == Item.rid)\
        .outerjoin(Task, Task.rid_items == Item.rid)\
        .outerjoin(Bug, Bug.rid_items == Item.rid)\
        .filter(
            and_(
                Item.is_deleted == 0,
                or_(
                    Item.type.in_([
                        ItemType.PROJECT.value,
                        ItemType.EVENT.value,
                        ItemType.FEATURE.value,
                        ItemType.STORY.value,
                        ItemType.BUG.value
                    ]),
                    Item.state == ItemState.ALERT.value
                )
            )
        )\
        .order_by(Item.path_sort)

        result = query.all()
        return result

    except Exception as e:
        raise e


def getItemRange(db: Session, id_project: int):
    try:
        query = db.query(
            Item.rid,
            Item.type,
            Item.state,
            Item.title,
            case(
                (Item.type == ItemType.PROJECT.value, Project.datetime_start),
                (Item.type == ItemType.EVENT.value, Event.datetime_end),
                (Item.type == ItemType.STORY.value, Story.datetime_start),
                else_=''
            ).label('datetime_start'),
            case(
                (Item.type == ItemType.PROJECT.value, Project.datetime_end),
                (Item.type == ItemType.EVENT.value, Event.datetime_end),
                (Item.type == ItemType.STORY.value, Story.datetime_end),
                else_=''
            ).label('datetime_end')
        )\
        .outerjoin(Project, Project.rid_items == Item.rid)\
        .outerjoin(Event, Event.rid_items == Item.rid)\
        .outerjoin(Feature, Feature.rid_items == Item.rid)\
        .outerjoin(Story, Story.rid_items == Item.rid)\
        .filter(
            Item.is_deleted == 0,
            Item.type.in_([
                ItemType.PROJECT.value,
                ItemType.EVENT.value,
                ItemType.STORY.value
            ])
        )\
        .order_by(Item.path_sort, Item.rid)

        result = query.all()
        return result

    except Exception as e:
        raise e


def updateItemState(db: Session, target: int, state: int):
    try:
        db.begin()
        item = db.query(
            Item
        )\
        .filter(Item.rid == target)

        item.update({
            Item.state: state
        })
        db.commit()

        item_updated = item.first()
        db.refresh(item_updated)
        return item_updated

    except Exception as e:
        db.rollback()
        raise e


def getProjects(db: Session):
    try:
        UserAlias = aliased(User)

        query = db.query(
            Item.rid,
            Item.id_project,
            Item.state,
            Item.risk,
            Item.title,
            Item.detail,
            Item.result,
            Item.datetime_entry,
            Item.datetime_update,
            UserAlias.rid.label('rid_users'),
            UserAlias.name.label('name'),
            Project.datetime_start.label('project_datetime_start'),
            Project.datetime_end.label('project_datetime_end'))\
        .outerjoin(UserAlias,  UserAlias.rid == Item.rid_users)\
        .outerjoin(Project, Project.rid_items == Item.rid)\
        .filter(
            Item.is_deleted == 0,
            Item.type == ItemType.PROJECT.value
        )\
        .order_by(Item.rid)

        result = query.all()
        return result

    except Exception as e:
        raise e


def createProject(db: Session, target: schema_item.ProjectCreate):
    try:
        datetime_current = getCurrentDatetime()

        db.begin()
        max_id_project = _createNextRID(db)

        item = Item(
            path_sort=_createSortPathProject(max_id_project),
            rid_users=target.rid_users,
            rid_users_review=None,
            id_project=max_id_project,
            type=ItemType.PROJECT.value,
            title=target.title,
            detail=target.detail,
            result='',
            datetime_entry=datetime_current,
            datetime_update=datetime_current
        )
        db.add(item)
        db.flush()

        addition = Project(
            rid_items=item.rid,
            datetime_start=target.project_datetime_start,
            datetime_end=target.project_datetime_end
        )
        db.add(addition)

        tree = Tree(
            rid_ancestor=max_id_project,
            rid_descendant=max_id_project,
            type=ItemType.PROJECT.value
        )
        db.add(tree)
        db.commit()

        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def updateProject(db: Session, target:schema_item.ProjectUpdate):
    try:
        param_item = ItemUpdateCommon(
            rid=target.rid,
            state=target.state,
            rid_users=target.rid_users,
            rid_users_review=target.rid_users_review,
            title=target.title,
            detail=target.detail,
            result=target.result
        )

        db.begin()
        item = _updateItem(db, param_item)

        addition = db.query(
            Project
        )\
        .filter(Project.rid_items == target.rid)

        addition.update({
            Project.datetime_start: target.project_datetime_start,
            Project.datetime_end: target.project_datetime_end
        })
        db.commit()
        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def deleteProject(db: Session, rid: int):
    try:
        _deleteItem(db, rid)

    except Exception as e:
        raise e


def createEvent(db: Session, target:schema_item.EventCreate):
    try:
        datetime_current = getCurrentDatetime()

        db.begin()
        item = Item(
            path_sort=_createSortPathEvent(db, target),
            id_project=target.id_project,
            rid_users=target.rid_users,
            rid_users_review=None,
            type=ItemType.EVENT.value,
            title=target.title,
            detail=target.detail,
            result='',
            datetime_entry=datetime_current,
            datetime_update=datetime_current
        )

        db.add(item)
        db.flush()

        addition = Event(
            rid_items=item.rid,
            datetime_end=target.event_datetime_end
        )
        db.add(addition)

        _createTree(db, ItemType.EVENT, target.rid_items, item.rid)
        db.flush()
        db.commit()

        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def updateEvent(db: Session, target:schema_item.EventUpdate):
    try:
        param_item = ItemUpdateCommon(
            rid=target.rid,
            state=target.state,
            rid_users=target.rid_users,
            rid_users_review=target.rid_users_review,
            title=target.title,
            detail=target.detail,
            result=target.result
        )

        db.begin()
        item = _updateItem(db, param_item)

        addition = db.query(
            Event
        )\
        .filter(Event.rid_items == target.rid)

        addition.update({
            Event.datetime_end: target.event_datetime_end
        })

        _updateSortPathEvent(db, target.rid, target.event_datetime_end)
        db.commit()
        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def deleteEvent(db: Session, rid: int):
    try:
        _deleteItem(db, rid)

    except Exception as e:
        raise e


def createFeature(db: Session, target:schema_item.FeatureCreate):
    try:
        datetime_current = getCurrentDatetime()

        db.begin()
        item = Item(
            path_sort=_createSortPathFeature(db, target),
            id_project=target.id_project,
            rid_users=target.rid_users,
            rid_users_review=None,
            type=ItemType.FEATURE.value,
            title=target.title,
            detail=target.detail,
            result='',
            datetime_entry=datetime_current,
            datetime_update=datetime_current
        )

        db.add(item)
        db.flush()

        addition = Feature(
            rid_items=item.rid
        )
        db.add(addition)

        _createTree(db, ItemType.FEATURE, target.rid_items, item.rid)
        db.flush()
        db.commit()

        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def updateFeature(db: Session, target:schema_item.FeatureUpdate):
    try:
        param_item = ItemUpdateCommon(
            rid=target.rid,
            state=target.state,
            rid_users=target.rid_users,
            rid_users_review=target.rid_users_review,
            title=target.title,
            detail=target.detail,
            result=target.result
        )

        db.begin()
        item = _updateItem(db, param_item)
        db.commit()
        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def deleteFeature(db: Session, rid: int):
    try:
        _deleteItem(db, rid)

    except Exception as e:
        raise e


def createStory(db: Session, target:schema_item.StoryCreate):
    try:
        datetime_current = getCurrentDatetime()

        db.begin()
        item = Item(
            path_sort=_createSortPathStory(db, target),
            id_project=target.id_project,
            rid_users=target.rid_users,
            rid_users_review=None,
            type=ItemType.STORY.value,
            title=target.title,
            detail=target.detail,
            result='',
            datetime_entry=datetime_current,
            datetime_update=datetime_current
        )

        db.add(item)
        db.flush()

        addition = Story(
            rid_items=item.rid,
            datetime_start=target.story_datetime_start,
            datetime_end=target.story_datetime_end
        )
        db.add(addition)

        _createTree(db, ItemType.STORY, target.rid_items, item.rid)
        db.flush()
        db.commit()

        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def updateStory(db: Session, target:schema_item.StoryUpdate):
    try:
        param_item = ItemUpdateCommon(
            rid=target.rid,
            state=target.state,
            rid_users=target.rid_users,
            rid_users_review=target.rid_users_review,
            title=target.title,
            detail=target.detail,
            result=target.result
        )

        db.begin()
        item = _updateItem(db, param_item)

        addition = db.query(
            Story
        )\
        .filter(Story.rid_items == target.rid)

        addition.update({
            Story.datetime_start: target.story_datetime_start,
            Story.datetime_end: target.story_datetime_end

        })

        _updateSortPathStory(db, target.rid, target.story_datetime_end)
        db.commit()
        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def deleteStory(db: Session, rid: int):
    try:
        _deleteItem(db, rid)

    except Exception as e:
        raise e


def createTask(db: Session, target:schema_item.TaskCreate):
    try:
        datetime_current = getCurrentDatetime()

        db.begin()
        item = Item(
            path_sort=_createSortPathTask(db, target),
            id_project=target.id_project,
            rid_users=target.rid_users,
            rid_users_review=None,
            type=ItemType.TASK.value,
            title=target.title,
            detail=target.detail,
            result='',
            datetime_entry=datetime_current,
            datetime_update=datetime_current
        )

        db.add(item)
        db.flush()

        addition = Task(
            rid_items=item.rid,
            type=target.task_type,
            workload=target.task_workload,
            number_completed=target.task_number_completed,
            number_total=target.task_number_total
        )
        db.add(addition)

        _createTree(db, ItemType.TASK, target.rid_items, item.rid)
        db.flush()

        _setRisk(db, item.rid)
        createSummaryItem(db, target.id_project, item.rid)
        createSummaryUser(db, target.id_project, target.rid_users)
        db.commit()

        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def updateTask(db: Session, target:schema_item.TaskUpdate):
    try:
        param_item = ItemUpdateCommon(
            rid=target.rid,
            state=target.state,
            rid_users=target.rid_users,
            rid_users_review=target.rid_users_review,
            title=target.title,
            detail=target.detail,
            result=target.result
        )

        db.begin()
        item = _updateItem(db, param_item)

        addition = db.query(
            Task
        )\
        .filter(Task.rid_items == target.rid)

        addition.update({
            Task.type: target.task_type,
            Task.workload: target.task_workload,
            Task.number_completed: target.task_number_completed,
            Task.number_total: target.task_number_total
        })

        id_project = db.query(
            Item.id_project
        )\
        .filter(Item.rid == target.rid)

        _setRisk(db, item.rid)
        createSummaryItem(db, id_project, item.rid)
        createSummaryUser(db, id_project, target.rid_users)
        db.commit()

        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def deleteTask(db: Session, rid: int):
    try:
        _deleteItem(db, rid)

    except Exception as e:
        raise e


def updateTaskPriority(db: Session, target:schema_item.TaskPriorityUpdate):
    try:
        db.begin()
        item = db.query(
            Item
        )\
        .filter(Item.rid == target.rid)

        item.update({
            Item.priority: target.priority
        })
        db.commit()

        item_updated = item.first()
        db.refresh(item_updated)
        return item_updated

    except Exception as e:
        db.rollback()
        raise e


def createBug(db: Session, target:schema_item.BugCreate):
    try:
        datetime_current = getCurrentDatetime()

        db.begin()
        item = Item(
            path_sort=_createSortPathBug(db, target),
            id_project=target.id_project,
            rid_users=target.rid_users,
            rid_users_review=None,
            type=ItemType.BUG.value,
            title=target.title,
            detail=target.detail,
            result='',
            datetime_entry=datetime_current,
            datetime_update=datetime_current
        )

        db.add(item)
        db.flush()

        addition = Bug(
            rid_items=item.rid,
            workload=target.bug_workload
        )
        db.add(addition)

        _createTree(db, ItemType.BUG, target.rid_items, item.rid)
        db.flush()

        _setRisk(db, item.rid)
        createSummaryItem(db, target.id_project, item.rid)
        createSummaryUser(db, target.id_project, target.rid_users)
        db.commit()

        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def updateBug(db: Session, target:schema_item.BugUpdate):
    try:
        param_item = ItemUpdateCommon(
            rid=target.rid,
            state=target.state,
            rid_users=target.rid_users,
            rid_users_review=target.rid_users_review,
            title=target.title,
            detail=target.detail,
            result=target.result
        )

        db.begin()
        item = _updateItem(db, param_item)

        addition = db.query(
            Bug
        )\
        .filter(Bug.rid_items == target.rid)

        addition.update({
            Bug.workload: target.bug_workload
        })

        id_project = db.query(
            Item.id_project
        )\
        .filter(Item.rid == target.rid)

        _setRisk(db, item.rid)
        createSummaryItem(db, id_project, item.rid)
        createSummaryUser(db, id_project, target.rid_users)
        db.commit()

        db.refresh(item)
        return item

    except Exception as e:
        db.rollback()
        raise e


def deleteBug(db: Session, rid: int):
    try:
        _deleteItem(db, rid)

    except Exception as e:
        raise e


def updateBugPriority(db: Session, target:schema_item.BugPriorityUpdate):
    try:
        db.begin()
        item = db.query(
            Item
        )\
        .filter(Item.rid == target.rid)

        item.update({
            Item.priority: target.priority
        })
        db.commit()

        item_updated = item.first()
        db.refresh(item_updated)
        return item_updated

    except Exception as e:
        db.rollback()
        raise e


def getAncestorsItemsRID(db: Session, rid: int):
    try:
        query = db.query(
            Tree.rid_ancestor.label('rid')
        )\
        .filter(Tree.rid_descendant == rid)\
        .filter(Tree.rid_descendant != Tree.rid_ancestor)\
        .order_by(Tree.rid_ancestor)

        result = query.all()
        return result

    except Exception as e:
        raise e


def getHierarchy(db: Session, id_project: int, visited=None):
    if visited is None:
        visited = set()

    if id_project in visited:
        return {}

    visited.add(id_project)

    UserAlias = aliased(User)

    ancestor = db.query(
        Item.rid,
        Item.type,
        Item.title,
        UserAlias.rid.label('rid_users'),
        UserAlias.name.label('name'),
        case(
            (Task.type == TaskType.WORKLOAD.value, Task.workload),
            (Task.type == TaskType.NUMBER.value,   35)
        ).label('task_workload'),
        Bug.workload.label('bug_workload')
    )\
    .select_from(Item)\
    .outerjoin(UserAlias,  UserAlias.rid == Item.rid_users)\
    .outerjoin(Task, Task.rid_items == Item.rid)\
    .outerjoin(Bug, Bug.rid_items == Item.rid)\
    .filter(Item.rid == id_project).first()

    descendants = db.query(
        Item.rid,
        Item.type,
        Item.title,
        UserAlias.rid.label('rid_users'),
        UserAlias.name.label('name'),
        case(
            (Task.type == TaskType.WORKLOAD.value, Task.workload),
            (Task.type == TaskType.NUMBER.value,   35)
        ).label('task_workload'),
        Bug.workload.label('bug_workload')
    )\
    .select_from(Item)\
    .join(Tree, Item.rid == Tree.rid_descendant)\
    .outerjoin(UserAlias,  UserAlias.rid == Item.rid_users)\
    .outerjoin(Task, Task.rid_items == Item.rid)\
    .outerjoin(Bug, Bug.rid_items == Item.rid)\
    .filter(Tree.rid_ancestor == id_project)\
    .all()

    children = [getHierarchy(db, desc.rid, visited) for desc in descendants]
    
    return {
        "rid": ancestor.rid,
        "rid_users": ancestor.rid_users,
        "name": ancestor.name,
        "type": ancestor.type,
        "title": ancestor.title,
        "workload_task": ancestor.task_workload,
        "workload_bug": ancestor.bug_workload,
        "children": [child for child in children if child]
    }


def getFrequency(db: Session, id_project):
    try:
        query = db.query(
            func.date(Item.datetime_entry).label('datetime_entry'),
            func.sum(case((Item.type == 5, 1), else_=0)).label('task_count'),
            func.sum(case((Item.type == 6, 1), else_=0)).label('bug_count'),
        )\
        .filter(
            Item.is_deleted == 0,
            Item.id_project == id_project,
            Item.type.in_([5, 6])
        )\
        .group_by(func.date(Item.datetime_entry))\
        .order_by(func.date(Item.datetime_entry))
    
        result = query.all()
        return result

    except Exception as e:
        raise e


def updateSummary(db: Session):
    try:
        db.begin()

        targets_item = db.query(
            Item.rid,
            Item.id_project
        )\
        .filter(
            Item.is_deleted == 0,
            Item.type.in_([5, 6]),
            Item.state != ItemState.COMPLETE.value,
        )\
        .all()

        for target in targets_item:
            createSummaryItem(db, target.id_project, target.rid)

        targets_user = db.query(
            Item.id_project,
            Item.rid_users
        )\
        .filter(
            Item.is_deleted == 0,
            Item.type.in_([5, 6]),
            Item.state != ItemState.COMPLETE.value,
        )\
        .group_by(
            Item.id_project,
            Item.rid_users
        )\
        .all()

        for target in targets_user:
            createSummaryUser(db, target.id_project, target.rid_users)

        db.commit()

    except Exception as e:
        raise e
