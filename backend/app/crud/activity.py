from sqlalchemy import text
from sqlalchemy.orm import Session

from crud.common import get_datetime_current
from schema import activity as schema_activity
from model.activity import Activity
from model.user import User


def get_activities(db: Session, rid_items: int, search_query: str = None):
    try:
        query = db.query(
            Activity.rid,
            Activity.activity,
            Activity.datetime_entry,
            Activity.datetime_update,
            User.rid.label('rid_users'),
            User.name.label('name')
        )\
        .outerjoin(User,  User.rid == Activity.rid_users)\
        .filter(
            Activity.is_deleted == 0,
            Activity.rid_items == rid_items
        )

        if search_query:
            fts_query = text("""
                SELECT rowid FROM activities_fts WHERE activities_fts.activity MATCH :search_query
            """)
            query = query.filter(Activity.rid.in_(fts_query)).params(search_query=search_query)

        query = query.order_by(Activity.rid)
        result = query.all()
        return result

    except Exception as e:
        raise e


def create_activity(db: Session, target:schema_activity.ActivityCreate):
    try:
        current_datetime = get_datetime_current()

        db.begin()
        activity = Activity(
            rid_items=target.rid_items,
            rid_users=target.rid_users,
            activity=target.activity,
            datetime_entry=current_datetime,
            datetime_update=current_datetime
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
        return activity

    except Exception as e:
        db.rollback()
        raise e


def update_activity(db: Session, target:schema_activity.ActivityUpdate):
    try:
        current_datetime = get_datetime_current()

        activity = db.query(
            Activity
        )\
        .filter(Activity.rid == target.rid)

        activity.update({
            Activity.activity: target.activity,
            Activity.datetime_update: current_datetime
        })

        activity_updated = activity.first()
        return activity_updated

    except Exception as e:
        db.rollback()
        raise e


def delete_activity(db: Session, rid: int):
    try:
        current_datetime = get_datetime_current()

        db.begin()
        item = db.query(
            Activity
        )\
        .filter(Activity.rid == rid)

        item.update({
            Activity.is_deleted: 1,
            Activity.datetime_update: current_datetime
        })
        db.commit()

    except Exception as e:
        raise e
