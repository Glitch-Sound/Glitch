from sqlalchemy import select, distinct, and_, or_, func, case, text
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import func

import sys
sys.path.append('~/app')

from crud.common import getWeekAgoDate, getCurrentDatetime, ItemType, ItemState, ExtractType, TaskType

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


def _createSortPathRoot(id_project: int):
    return id_project * 10000000000000


def _createSortPath(db: Session, type: ItemType, rid_parent: int):
    try:
        path_sort_parent      = db.query(
            Item.path_sort
        )\
        .filter(Item.rid == rid_parent)\
        .scalar()

        count_rid_descendants = db.query(
            Tree.rid_descendant
        )\
        .filter(Tree.rid_ancestor == rid_parent)\
        .count()

        path_sort = path_sort_parent
        match type:
            case ItemType.EVENT:
                path_sort += (count_rid_descendants * 1000000000)

            case ItemType.FEATURE:
                path_sort += (count_rid_descendants * 100000)

            case ItemType.STORY:
                path_sort += (count_rid_descendants * 10)

            case ItemType.TASK | ItemType.BUG:
                path_sort += (type.value)

        return path_sort

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
                Item.risk_factors: 0,
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
                        400 <= Item.risk
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
                fts_query_title = text("""
                    SELECT rowid FROM items_fts WHERE items_fts.title MATCH :search_query
                """)
                fts_query_detail = text("""
                    SELECT rowid FROM items_fts WHERE items_fts.detail MATCH :search_query
                """)
                fts_query_result= text("""
                    SELECT rowid FROM items_fts WHERE items_fts.result MATCH :search_query
                """)

                subquery_target = (
                    select(Item.rid)
                    .where(
                        and_(
                            Item.id_project == params.id_project,
                            or_(
                                Item.rid.in_(fts_query_title),
                                Item.rid.in_(fts_query_detail),
                                Item.rid.in_(fts_query_result)
                            )
                        )
                    )
                )\
                .params(search_query=params.search)\
                .subquery()

                cte_extruct = db.query(
                    distinct(Tree.rid_ancestor).label('rid')
                )\
                .where(Tree.rid_descendant.in_(select(subquery_target)))

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
            Item.risk_factors,
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
        .order_by(Item.path_sort, Item.priority.desc())

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


def getProjects(db: Session):
    try:
        UserAlias = aliased(User)

        query = db.query(
            Item.rid,
            Item.id_project,
            Item.state,
            Item.risk,
            Item.risk_factors,
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
        max_id_project = db.query(
            func.max(Item.id_project)
        )\
        .scalar()

        if max_id_project is None:
            max_id_project = 0
        max_id_project += 1

        item = Item(
            path_sort=_createSortPathRoot(max_id_project),
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
            datetime_start=target.datetime_start,
            datetime_end=target.datetime_end
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
            Project.datetime_start: target.datetime_start,
            Project.datetime_end: target.datetime_end
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
            path_sort=_createSortPath(db, ItemType.EVENT, target.rid_items),
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
            datetime_end=target.datetime_end
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
            Event.datetime_end: target.datetime_end
        })
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
            path_sort=_createSortPath(db, ItemType.FEATURE, target.rid_items),
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
            path_sort=_createSortPath(db, ItemType.STORY, target.rid_items),
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
            datetime_start=target.datetime_start,
            datetime_end=target.datetime_end
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
            Story.datetime_start: target.datetime_start,
            Story.datetime_end: target.datetime_end

        })

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
            path_sort=_createSortPath(db, ItemType.TASK, target.rid_items),
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
            type=target.type,
            workload=target.workload,
            number_completed=target.number_completed,
            number_total=target.number_total
        )
        db.add(addition)

        _createTree(db, ItemType.TASK, target.rid_items, item.rid)
        db.flush()

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
            Task.type: target.type,
            Task.workload: target.workload,
            Task.number_completed: target.number_completed,
            Task.number_total: target.number_total
        })

        id_project = db.query(
            Item.id_project
        )\
        .filter(Item.rid == target.rid)

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


def createBug(db: Session, target:schema_item.BugCreate):
    try:
        datetime_current = getCurrentDatetime()

        db.begin()
        item = Item(
            path_sort=_createSortPath(db, ItemType.BUG, target.rid_items),
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
            workload=target.workload
        )
        db.add(addition)

        _createTree(db, ItemType.BUG, target.rid_items, item.rid)
        db.flush()

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
            Bug.workload: target.workload
        })

        id_project = db.query(
            Item.id_project
        )\
        .filter(Item.rid == target.rid)

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


def getItemsNotice(db: Session, id_project, select_date):
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
            Item.state != ItemState.COMPLETE.value,
            Story.datetime_start <= select_date
        )

        cte_extruct_descendant = db.query(
            Tree.rid_descendant.label('rid')
        )\
        .join(Item, Item.rid == Tree.rid_ancestor)\
        .join(Story, Item.rid == Story.rid_items)\
        .where(
            Item.id_project == id_project,
            Item.state != ItemState.COMPLETE.value,
            Story.datetime_start <= select_date
        )

        cte_extruct = cte_extruct_ancestor.union(cte_extruct_descendant).cte(name='targets')

        query = db.query(
            Item.rid,
            Item.id_project,
            Item.type,
            Item.state,
            Item.risk,
            Item.risk_factors,
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
    return
