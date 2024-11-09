from sqlalchemy import desc, func, case, cast, Integer
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import func

import sys
sys.path.append('~/app')

from crud.common import getCurrentDate, getPreviousDate, ItemType, ItemState

from model.summary_item import SummaryItem
from model.summary_user import SummaryUser
from model.item import Item
from model.user import User
from model.tree import Tree
from model.task import Task
from model.bug import Bug


def getSummariesProject(db: Session, id_project: int):
    try:
        query = db.query(
            SummaryItem.rid_items.label('rid'),
            SummaryItem.risk,
            SummaryItem.task_count_idle,
            SummaryItem.task_count_run,
            SummaryItem.task_count_alert,
            SummaryItem.task_count_review,
            SummaryItem.task_count_complete,
            SummaryItem.task_count_total,
            SummaryItem.task_workload_total,
            SummaryItem.task_number_completed,
            SummaryItem.task_number_total,
            SummaryItem.bug_count_idle,
            SummaryItem.bug_count_run,
            SummaryItem.bug_count_alert,
            SummaryItem.bug_count_review,
            SummaryItem.bug_count_complete,
            SummaryItem.bug_count_total,
            SummaryItem.bug_workload_total,
            SummaryItem.date_entry
        )\
        .filter(SummaryItem.id_project == id_project)\
        .order_by(SummaryItem.date_entry)

        result = query.all()
        return result
    except Exception as e:
        raise e


def getSummariesItem(db: Session, rid: int):
    try:
        query = db.query(
            SummaryItem.rid_items.label('rid'),
            SummaryItem.risk,
            SummaryItem.task_count_idle,
            SummaryItem.task_count_run,
            SummaryItem.task_count_alert,
            SummaryItem.task_count_review,
            SummaryItem.task_count_complete,
            SummaryItem.task_count_total,
            SummaryItem.task_workload_total,
            SummaryItem.task_number_completed,
            SummaryItem.task_number_total,
            SummaryItem.bug_count_idle,
            SummaryItem.bug_count_run,
            SummaryItem.bug_count_alert,
            SummaryItem.bug_count_review,
            SummaryItem.bug_count_complete,
            SummaryItem.bug_count_total,
            SummaryItem.bug_workload_total,
            SummaryItem.date_entry
        )\
        .filter(SummaryItem.rid_items == rid)\
        .order_by(SummaryItem.date_entry)

        result = query.all()
        return result

    except Exception as e:
        raise e


def getSummariesUser(db: Session, id_project: int, rid_users: int):
    try:
        UserAlias = aliased(User)

        query = db.query(
            SummaryUser.rid,
            SummaryUser.id_project,
            UserAlias.rid.label('rid_users'),
            UserAlias.name.label('name'),
            SummaryUser.risk,
            SummaryUser.task_count_idle,
            SummaryUser.task_count_run,
            SummaryUser.task_count_alert,
            SummaryUser.task_count_review,
            SummaryUser.task_count_complete,
            SummaryUser.task_count_total,
            SummaryUser.task_workload_total,
            SummaryUser.task_number_completed,
            SummaryUser.task_number_total,
            SummaryUser.bug_count_idle,
            SummaryUser.bug_count_run,
            SummaryUser.bug_count_alert,
            SummaryUser.bug_count_review,
            SummaryUser.bug_count_complete,
            SummaryUser.bug_count_total,
            SummaryUser.bug_workload_total,
            SummaryUser.date_entry
        )\
        .join(UserAlias,  UserAlias.rid == SummaryUser.rid_users)\
        .filter(
            SummaryUser.rid_users  == rid_users,
            SummaryUser.id_project == id_project
        )\
        .order_by(SummaryUser.date_entry)

        result = query.all()
        return result

    except Exception as e:
        raise e


def createSummaryItem(db: Session, id_project: int, rid_target: int):
    try:
        trees = db.query(
            Tree
        )\
        .filter(Tree.rid_descendant == rid_target)\
        .order_by(desc(Tree.rid_ancestor))\
        .all()

        if not trees:
            raise

        for tree in trees:
            if tree.rid_ancestor == tree.rid_descendant:
                continue

            list_sum_risk = db.query(
                func.sum(Item.risk).label('risk'),
            )\
            .select_from(Tree)\
            .join(Item, Tree.rid_descendant == Item.rid)\
            .filter(
                Tree.rid_ancestor   == tree.rid_ancestor,
                Tree.rid_descendant != tree.rid_ancestor
            )\
            .all()

            list_sum_workload = db.query(
                func.sum(Task.workload).label('task_workload'),
                func.sum(Bug.workload).label('bug_workload')
            )\
            .select_from(Tree)\
            .join(Item, Tree.rid_descendant == Item.rid)\
            .outerjoin(Task, Tree.rid_descendant == Task.rid_items)\
            .outerjoin(Bug,  Tree.rid_descendant == Bug.rid_items)\
            .filter(
                Tree.rid_ancestor   == tree.rid_ancestor,
                Tree.rid_descendant != tree.rid_ancestor,
                Item.state != ItemState.IDLE.value
            )\
            .all()

            list_sum_number = db.query(
                func.sum(Task.number_completed).label('task_number_completed'),
                func.sum(Task.number_total).label('task_number_total')
            )\
            .select_from(Tree)\
            .outerjoin(Task, Tree.rid_descendant == Task.rid_items)\
            .outerjoin(Bug,  Tree.rid_descendant == Bug.rid_items)\
            .filter(
                Tree.rid_ancestor   == tree.rid_ancestor,
                Tree.rid_descendant != tree.rid_ancestor
            )\
            .all()
 
            list_count = db.query(
                Item.type,
                Item.state,
                func.count(Item.rid).label('count')
            )\
            .select_from(Tree)\
            .join(Item, Tree.rid_descendant == Item.rid)\
            .filter(
                Tree.rid_ancestor   == tree.rid_ancestor,
                Tree.rid_descendant != tree.rid_ancestor
            )\
            .group_by(Item.type, Item.state)\
            .all()

            result_sum, result_count = _getSummary(list_sum_risk, list_sum_workload, list_sum_number, list_count)

            summary_item = db.query(SummaryItem).filter(
                SummaryItem.rid_items == tree.rid_ancestor,
            ).all()

            if not summary_item:
                date_previous = getPreviousDate()
                summary = SummaryItem(
                    id_project=id_project,
                    rid_items=tree.rid_ancestor,
                    risk=0,
                    task_count_idle=0,
                    task_count_run=0,
                    task_count_alert=0,
                    task_count_review=0,
                    task_count_complete=0,
                    task_count_total=0,
                    task_workload_total=0,
                    task_number_completed=0,
                    task_number_total=0,
                    bug_count_idle=0,
                    bug_count_run=0,
                    bug_count_alert=0,
                    bug_count_review=0,
                    bug_count_complete=0,
                    bug_count_total=0,
                    bug_workload_total=0,
                    date_entry=date_previous
                )
                db.add(summary)

            date_current = getCurrentDate()
            summary_item = db.query(
                SummaryItem
            )\
            .filter(
                SummaryItem.rid_items  == tree.rid_ancestor,
                SummaryItem.date_entry == date_current
            ).all()

            if not summary_item:
                summary = SummaryItem(
                    id_project=id_project,
                    rid_items=tree.rid_ancestor,
                    risk=result_sum['risk'],
                    task_count_idle=result_count['task_count_idle'],
                    task_count_run=result_count['task_count_run'],
                    task_count_alert=result_count['task_count_alert'],
                    task_count_review=result_count['task_count_review'],
                    task_count_complete=result_count['task_count_complete'],
                    task_count_total=result_count['task_count_total'],
                    task_workload_total=result_sum['task_workload'],
                    task_number_completed=result_sum['task_number_completed'],
                    task_number_total=result_sum['task_number_total'],
                    bug_count_idle=result_count['bug_count_idle'],
                    bug_count_run=result_count['bug_count_run'],
                    bug_count_alert=result_count['bug_count_alert'],
                    bug_count_review=result_count['bug_count_review'],
                    bug_count_complete=result_count['bug_count_complete'],
                    bug_count_total=result_count['bug_count_total'],
                    bug_workload_total=result_sum['bug_workload'],
                    date_entry=date_current
                )
                db.add(summary)

            else:
                summary = db.query(
                    SummaryItem
                )\
                .filter(
                    SummaryItem.rid_items  == tree.rid_ancestor,
                    SummaryItem.date_entry == date_current
                )

                summary.update({
                    SummaryItem.risk: result_sum['risk'],
                    SummaryItem.task_count_idle: result_count['task_count_idle'],
                    SummaryItem.task_count_run: result_count['task_count_run'],
                    SummaryItem.task_count_alert: result_count['task_count_alert'],
                    SummaryItem.task_count_review: result_count['task_count_review'],
                    SummaryItem.task_count_complete: result_count['task_count_complete'],
                    SummaryItem.task_count_total: result_count['task_count_total'],
                    SummaryItem.task_workload_total: result_sum['task_workload'],
                    SummaryItem.task_number_completed: result_sum['task_number_completed'],
                    SummaryItem.task_number_total: result_sum['task_number_total'],
                    SummaryItem.bug_count_idle: result_count['bug_count_idle'],
                    SummaryItem.bug_count_run: result_count['bug_count_run'],
                    SummaryItem.bug_count_alert: result_count['bug_count_alert'],
                    SummaryItem.bug_count_review: result_count['bug_count_review'],
                    SummaryItem.bug_count_complete: result_count['bug_count_complete'],
                    SummaryItem.bug_count_total: result_count['bug_count_total'],
                    SummaryItem.bug_workload_total: result_sum['bug_workload']
                })

    except Exception as e:
        raise e


def createSummaryUser(db: Session, id_project: int, rid_users: int):
    try:
        list_sum_risk = db.query(
            func.sum(Item.risk).label('risk'),
        )\
        .select_from(Item)\
        .filter(
            Item.id_project == id_project.scalar_subquery(),
            Item.rid_users  == rid_users,
            Item.type.in_([ItemType.TASK.value, ItemType.BUG.value])
        )\
        .all()

        list_sum_workload = db.query(
            func.sum(Task.workload).label('task_workload'),
            func.sum(Bug.workload).label('bug_workload')
        )\
        .select_from(Item)\
        .outerjoin(Task, Item.rid == Task.rid_items)\
        .outerjoin(Bug,  Item.rid == Bug.rid_items)\
        .filter(
            Item.id_project == id_project.scalar_subquery(),
            Item.rid_users  == rid_users,
            Item.type.in_([ItemType.TASK.value, ItemType.BUG.value]),
            Item.state != ItemState.IDLE.value
        )\
        .all()

        list_sum_number = db.query(
            func.sum(Task.number_completed).label('task_number_completed'),
            func.sum(Task.number_total).label('task_number_total')
        )\
        .select_from(Item)\
        .outerjoin(Task, Item.rid == Task.rid_items)\
        .outerjoin(Bug,  Item.rid == Bug.rid_items)\
        .filter(
            Item.id_project == id_project.scalar_subquery(),
            Item.rid_users  == rid_users,
            Item.type.in_([ItemType.TASK.value, ItemType.BUG.value])
        )\
        .all()

        list_count = db.query(
            Item.type,
            Item.state,
            func.count(Item.rid).label('count')
        )\
        .select_from(Item)\
        .filter(
            Item.id_project == id_project.scalar_subquery(),
            Item.rid_users  == rid_users,
            Item.type.in_([ItemType.TASK.value, ItemType.BUG.value])
        )\
        .group_by(Item.type, Item.state)\
        .all()

        result_sum, result_count = _getSummary(list_sum_risk, list_sum_workload, list_sum_number, list_count)

        summary_user = db.query(
            SummaryUser
        )\
        .filter(
            SummaryUser.rid_users  == rid_users,
            SummaryUser.id_project == id_project.scalar_subquery()
        ).all()

        if not summary_user:
            date_previous = getPreviousDate()
            summary = SummaryUser(
                rid_users=rid_users,
                id_project=id_project,
                risk=0,
                task_count_idle=0,
                task_count_run=0,
                task_count_alert=0,
                task_count_review=0,
                task_count_complete=0,
                task_count_total=0,
                task_workload_total=0,
                task_number_completed=0,
                task_number_total=0,
                bug_count_idle=0,
                bug_count_run=0,
                bug_count_alert=0,
                bug_count_review=0,
                bug_count_complete=0,
                bug_count_total=0,
                bug_workload_total=0,
                date_entry=date_previous
            )
            db.add(summary)

        date_current = getCurrentDate()

        summary_user = db.query(
            SummaryUser
        )\
        .filter(
            SummaryUser.rid_users  == rid_users,
            SummaryUser.id_project == id_project.scalar_subquery(),
            SummaryUser.date_entry == date_current
        ).all()

        if not summary_user:
            summary = SummaryUser(
                rid_users=rid_users,
                id_project=id_project,
                risk=result_sum['risk'],
                task_count_idle=result_count['task_count_idle'],
                task_count_run=result_count['task_count_run'],
                task_count_alert=result_count['task_count_alert'],
                task_count_review=result_count['task_count_review'],
                task_count_complete=result_count['task_count_complete'],
                task_count_total=result_count['task_count_total'],
                task_workload_total=result_sum['task_workload'],
                task_number_completed=result_sum['task_number_completed'],
                task_number_total=result_sum['task_number_total'],
                bug_count_idle=result_count['bug_count_idle'],
                bug_count_run=result_count['bug_count_run'],
                bug_count_alert=result_count['bug_count_alert'],
                bug_count_review=result_count['bug_count_review'],
                bug_count_complete=result_count['bug_count_complete'],
                bug_count_total=result_count['bug_count_total'],
                bug_workload_total=result_sum['bug_workload'],
                date_entry=date_current
            )
            db.add(summary)

        else:
            summary = db.query(
                SummaryUser
            )\
            .filter(
                SummaryUser.rid_users  == rid_users,
                SummaryUser.id_project == id_project.scalar_subquery(),
                SummaryUser.date_entry == date_current
            )

 
            summary.update({
                SummaryUser.risk: result_sum['risk'],
                SummaryUser.task_count_idle: result_count['task_count_idle'],
                SummaryUser.task_count_run: result_count['task_count_run'],
                SummaryUser.task_count_alert: result_count['task_count_alert'],
                SummaryUser.task_count_review: result_count['task_count_review'],
                SummaryUser.task_count_complete: result_count['task_count_complete'],
                SummaryUser.task_count_total: result_count['task_count_total'],
                SummaryUser.task_workload_total: result_sum['task_workload'],
                SummaryUser.task_number_completed: result_sum['task_number_completed'],
                SummaryUser.task_number_total: result_sum['task_number_total'],
                SummaryUser.bug_count_idle: result_count['bug_count_idle'],
                SummaryUser.bug_count_run: result_count['bug_count_run'],
                SummaryUser.bug_count_alert: result_count['bug_count_alert'],
                SummaryUser.bug_count_review: result_count['bug_count_review'],
                SummaryUser.bug_count_complete: result_count['bug_count_complete'],
                SummaryUser.bug_count_total: result_count['bug_count_total'],
                SummaryUser.bug_workload_total: result_sum['bug_workload']
            })

    except Exception as e:
        raise e


def _getSummary(list_sum_risk: any, list_sum_workload: any, list_sum_number: any, list_count: any):
    result_sum = {
        'risk'                  : 0,
        'task_workload'         : 0,
        'task_number_completed' : 0,
        'task_number_total'     : 0,
        'bug_workload'          : 0
    }

    print(list_sum_risk)


    if list_sum_risk[0].risk:
        result_sum['risk'] = list_sum_risk[0].risk

    if list_sum_workload[0].task_workload:
        result_sum['task_workload'] = list_sum_workload[0].task_workload

    if list_sum_workload[0].bug_workload:
        result_sum['bug_workload'] = list_sum_workload[0].bug_workload

    if list_sum_number[0].task_number_completed:
        result_sum['task_number_completed'] = list_sum_number[0].task_number_completed

    if list_sum_number[0].task_number_total:
        result_sum['task_number_total'] = list_sum_number[0].task_number_total

    result_count = {
        'task_count_idle'     : 0,
        'task_count_run'      : 0,
        'task_count_alert'    : 0,
        'task_count_review'   : 0,
        'task_count_complete' : 0,
        'task_count_total'    : 0,
        'bug_count_idle'      : 0,
        'bug_count_run'       : 0,
        'bug_count_alert'     : 0,
        'bug_count_review'    : 0,
        'bug_count_complete'  : 0,
        'bug_count_total'     : 0
    }

    sum_task = 0
    sum_bug  = 0
    for target in list_count:
        if   target.type == ItemType.TASK.value:
            match target.state:
                case ItemState.IDLE.value:
                    result_count['task_count_idle'] = target.count
                    sum_task += target.count
                case ItemState.RUN.value:
                    result_count['task_count_run'] = target.count
                    sum_task += target.count
                case ItemState.ALERT.value:
                    result_count['task_count_alert'] = target.count
                    sum_task += target.count
                case ItemState.REVIEW.value:
                    result_count['task_count_review'] = target.count
                    sum_task += target.count
                case ItemState.COMPLETE.value:
                    result_count['task_count_complete'] = target.count
                    sum_task += target.count

        elif target.type == ItemType.BUG.value:
            match target.state:
                case ItemState.IDLE.value:
                    result_count['bug_count_idle'] = target.count
                    sum_bug += target.count
                case ItemState.RUN.value:
                    result_count['bug_count_run'] = target.count
                    sum_bug += target.count
                case ItemState.ALERT.value:
                    result_count['bug_count_alert'] = target.count
                    sum_bug += target.count
                case ItemState.REVIEW.value:
                    result_count['bug_count_review'] = target.count
                    sum_bug += target.count
                case ItemState.COMPLETE.value:
                    result_count['bug_count_complete'] = target.count
                    sum_bug += target.count

    result_count['task_count_total'] = sum_task
    result_count['bug_count_total']  = sum_bug

    return result_sum, result_count
