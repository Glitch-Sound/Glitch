from pydantic import BaseModel
from typing import List, Optional


class RID(BaseModel):
    rid: int

    class Config:
        from_attributes = True


class Item(BaseModel):
    rid: int
    id_project: int
    type: int
    state: int
    risk: int
    risk_factors: int
    priority: int
    title: str
    detail: str
    result: str
    datetime_entry: str
    datetime_update: str
    rid_users: int
    name: Optional[str] = None
    rid_users_review: Optional[int] = None
    name_review: Optional[str] = None
    project_datetime_start: Optional[str] = None
    project_datetime_end: Optional[str] = None
    event_datetime_end: Optional[str] = None
    story_datetime_start: Optional[str] = None
    story_datetime_end: Optional[str] = None
    task_type: Optional[int] = None
    task_workload: Optional[int] = None
    task_number_completed: Optional[int] = None
    task_number_total: Optional[int] = None
    bug_workload: Optional[int] = None

    class Config:
        from_attributes = True


class ItemRange(BaseModel):
    rid: int
    type: int
    state: int
    title: str
    datetime_start: str
    datetime_end: str

    class Config:
        from_attributes = True 


class StateUpdate(BaseModel):
    rid: int
    state: int

    class Config:
        from_attributes = True
    

class Project(BaseModel):
    rid: int
    id_project: int
    state: int
    risk: int
    risk_factors: int
    title: str
    detail: str
    result: str
    datetime_entry: str
    datetime_update: str
    rid_users: int
    name: Optional[str] = None
    project_datetime_start: Optional[str] = None
    project_datetime_end: Optional[str] = None

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    rid_users: int
    title: str
    detail: str
    project_datetime_start: str
    project_datetime_end: str

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    rid: int
    state: int
    rid_users: int
    rid_users_review: Optional[int] = None
    title: str
    detail: str
    result: str
    project_datetime_start: str
    project_datetime_end: str

    class Config:
        from_attributes = True


class EventCreate(BaseModel):
    id_project: int
    rid_items: int
    rid_users: int
    title: str
    detail: str
    event_datetime_end: str

    class Config:
        from_attributes = True


class EventUpdate(BaseModel):
    rid: int
    state: int
    rid_users: int
    rid_users_review: Optional[int] = None
    title: str
    detail: str
    result: str
    event_datetime_end: str

    class Config:
        from_attributes = True


class FeatureCreate(BaseModel):
    id_project: int
    rid_items: int
    rid_users: int
    title: str
    detail: str

    class Config:
        from_attributes = True


class FeatureUpdate(BaseModel):
    rid: int
    state: int
    rid_users: int
    rid_users_review: Optional[int] = None
    title: str
    detail: str
    result: str

    class Config:
        from_attributes = True


class StoryCreate(BaseModel):
    id_project: int
    rid_items: int
    rid_users: int
    title: str
    detail: str
    story_datetime_start: str
    story_datetime_end: str

    class Config:
        from_attributes = True


class StoryUpdate(BaseModel):
    rid: int
    state: int
    rid_users: int
    rid_users_review: Optional[int] = None
    title: str
    detail: str
    result: str
    story_datetime_start: str
    story_datetime_end: str

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    id_project: int
    rid_items: int
    rid_users: int
    title: str
    detail: str
    task_type: int
    task_workload: int
    task_number_completed: int
    task_number_total: int

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    rid: int
    state: int
    rid_users: int
    rid_users_review: Optional[int] = None
    title: str
    detail: str
    result: str
    task_type: int
    task_workload: int
    task_number_completed: int
    task_number_total: int

    class Config:
        from_attributes = True


class BugCreate(BaseModel):
    id_project: int
    rid_items: int
    rid_users: int
    title: str
    detail: str
    bug_workload: int

    class Config:
        from_attributes = True


class BugUpdate(BaseModel):
    rid: int
    state: int
    rid_users: int
    rid_users_review: Optional[int] = None
    title: str
    detail: str
    result: str
    bug_workload: int

    class Config:
        from_attributes = True
