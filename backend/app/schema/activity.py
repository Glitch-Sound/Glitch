from pydantic import BaseModel
from typing import Optional


class Activity(BaseModel):
    rid: int
    activity: str
    datetime_entry: str
    datetime_update: str
    rid_users: int
    name: Optional[str] = None

    class Config:
        from_attributes = True


class ActivityCreate(BaseModel):
    rid_items: int
    rid_users: int
    activity: str

    class Config:
        from_attributes = True


class ActivityUpdate(BaseModel):
    rid: int
    activity: str

    class Config:
        from_attributes = True
