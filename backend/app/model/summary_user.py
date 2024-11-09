from sqlalchemy import Column, ForeignKey, String, Integer, Index
from sqlalchemy.orm import relationship

import sys
sys.path.append('~/app')

from database import Base


class SummaryUser(Base):
    __tablename__ = 'summaries_user'

    rid                   = Column(Integer, primary_key=True)
    rid_users             = Column(Integer, ForeignKey('users.rid'))
    id_project            = Column(Integer, default=0)
    risk                  = Column(Integer, default=0)
    task_count_idle       = Column(Integer, default=0)
    task_count_run        = Column(Integer, default=0)
    task_count_alert      = Column(Integer, default=0)
    task_count_review     = Column(Integer, default=0)
    task_count_complete   = Column(Integer, default=0)
    task_count_total      = Column(Integer, default=0)
    task_workload_total   = Column(Integer, default=0)
    task_number_completed = Column(Integer, default=0)
    task_number_total     = Column(Integer, default=0)
    bug_count_idle        = Column(Integer, default=0)
    bug_count_run         = Column(Integer, default=0)
    bug_count_alert       = Column(Integer, default=0)
    bug_count_review      = Column(Integer, default=0)
    bug_count_complete    = Column(Integer, default=0)
    bug_count_total       = Column(Integer, default=0)
    bug_workload_total    = Column(Integer, default=0)
    date_entry            = Column(String,  default='')

    user  = relationship('User', back_populates='summaries_user')

    __table_args__ = (
        Index('idx_summaries_user_01', 'rid_users', 'id_project', 'date_entry'),
    )
