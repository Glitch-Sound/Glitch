from pydantic import BaseModel
from typing import Optional


class SummaryItem(BaseModel):
    rid: int
    risk: int
    task_count_idle: int
    task_count_run: int
    task_count_alert: int
    task_count_review: int
    task_count_complete: int
    task_count_total: int
    task_workload_total: int
    task_number_completed: int
    task_number_total: int
    bug_count_idle: int
    bug_count_run: int
    bug_count_alert: int
    bug_count_review: int
    bug_count_complete: int
    bug_count_total: int
    bug_workload_total: int
    date_entry: str

    class Config:
        from_attributes = True


class SummaryUser(BaseModel):
    rid: int
    id_project: int
    rid_users: int
    name: Optional[str] = None
    risk: int
    task_count_idle: int
    task_count_run: int
    task_count_alert: int
    task_count_review: int
    task_count_complete: int
    task_count_total: int
    task_workload_total: int
    task_number_completed: int
    task_number_total: int
    bug_count_idle: int
    bug_count_run: int
    bug_count_alert: int
    bug_count_review: int
    bug_count_complete: int
    bug_count_total: int
    bug_workload_total: int
    date_entry: str

    class Config:
        from_attributes = True
