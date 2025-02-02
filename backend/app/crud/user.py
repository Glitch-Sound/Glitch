from enum import Enum
from typing import List

import bcrypt
from sqlalchemy.orm import Session, aliased

from schema import user as schema_user
from model.user import User
from model.item import Item
from model.project import Project
from model.member import Member


class Authority(Enum):
    USER  = 0
    ADMIN = 1


def _create_hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def _verify_hash_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_users(db: Session):
    try:
        query = db.query(
            User
        )\
        .filter(User.is_deleted == 0)\
        .order_by(User.rid)

        result = query.all()
        return result

    except Exception as e:
        raise e


def get_users_project(db: Session, id_project: int):
    try:
        alias_user = aliased(User)

        cte_target = (
            db.query(
                Item.rid_users.label('rid_users')
            )
            .filter(
                Item.is_deleted == 0,
                Item.id_project == id_project
            )
            .group_by(Item.rid_users)
            .order_by(Item.rid_users)
            .cte('target')
        )

        query = (
            db.query(
                alias_user
            )\
            .join(cte_target, alias_user.rid == cte_target.c.rid_users)
            .filter(alias_user.is_deleted == 0)
            .order_by(alias_user.rid)
        )

        result = query.all()
        return result

    except Exception as e:
        raise e


def get_user(db: Session, rid_users: int):
    try:
        query = db.query(
            User
        )\
        .filter(
            User.is_deleted == 0,
            User.rid == rid_users
        )

        result = query.one()
        return result

    except Exception as e:
        raise e


def create_user(db: Session, target: schema_user.UserCreate):
    try:
        user = User(
             user=target.user,
             password=_create_hash_password(target.password),
             name=target.name,
             is_admin=target.is_admin
        )
        db.begin()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except Exception as e:
        db.rollback()
        raise e


def update_user(db: Session, target: schema_user.UserUpdate):
    try:
        db.begin()
        user = db.query(
            User
        )\
        .filter(User.rid == target.rid)

        user.update({
            User.user: target.user,
            User.password: _create_hash_password(target.password),
            User.name: target.name,
            User.is_admin: target.is_admin
        })
        db.commit()

        user_updated = user.first()
        db.refresh(user_updated)
        return user_updated

    except Exception as e:
        db.rollback()
        raise e


def delete_user(db: Session, rid: int):
    try:
        db.begin()
        user = db.query(
            User
        )\
        .filter(User.rid == rid)

        user.update({
            User.is_deleted: 1
        })
        db.commit()

    except Exception as e:
        db.rollback()
        raise e


def login(db: Session, target: schema_user.Login):
    try:
        user = db.query(
            User
        )\
        .filter(User.user == target.user)\
        .first()

        if user is None:
            return None

        if not _verify_hash_password(target.password, user.password):
            return None

        return user

    except Exception as e:
        raise e


def get_members(db: Session, id_project: int):
    try:
        query = (
            db.query(
                User
            )\
            .join(Member, Member.rid_users == User.rid)
            .join(Project, Project.rid == Member.rid_projects)
            .join(Item, Item.rid == Project.rid_items)
            .filter(
                User.is_deleted == 0,
                Item.id_project == id_project
            )
            .order_by(User.rid)
        )

        result = query.all()
        return result

    except Exception as e:
        raise e


def create_members(db: Session, id_project: int, targets: List[schema_user.MemberCreate]):
    try:
        db.begin()

        db.query(
            Member
        )\
        .join(Member, Member.rid_users == User.rid)\
        .join(Project, Project.rid == Member.rid_projects)\
        .join(Item, Item.rid == Project.rid_items)\
        .filter(
            Item.id_projects == id_project
        )\
        .delete(synchronize_session=False)

        for target in targets:
            user = Member(
                rid_projects=id_project,
                rid_users=target.rid
            )
            db.add(user)

        db.commit()

        return get_members(db, id_project)

    except Exception as e:
        db.rollback()
        raise e
