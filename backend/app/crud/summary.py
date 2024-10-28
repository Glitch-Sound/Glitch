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
