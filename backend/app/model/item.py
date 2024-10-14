from sqlalchemy import Column, ForeignKey, Integer, String, Index
from sqlalchemy.orm import relationship

import sys
sys.path.append('~/app')

from database import Base


class Item(Base):
    __tablename__ = 'items'

    rid              = Column(Integer, primary_key=True)
    rid_users        = Column(Integer, ForeignKey('users.rid'))
    rid_users_review = Column(Integer, ForeignKey('users.rid'), nullable=True)
    path_sort        = Column(Integer, default=0, index=True)
    id_project       = Column(Integer, default=0, index=True)
    type             = Column(Integer, default=0, index=True)
    state            = Column(Integer, default=1, index=True)
    risk             = Column(Integer, default=0, index=True)
    risk_factors     = Column(Integer, default=0)
    priority         = Column(Integer, default=0, index=True)
    title            = Column(String,  default='')
    detail           = Column(String,  default='')
    result           = Column(String,  default='')
    datetime_entry   = Column(String,  default='', index=True)
    datetime_update  = Column(String,  default='', index=True)
    is_deleted       = Column(Integer, default=0)

    ancestors    = relationship('Tree', foreign_keys='Tree.rid_descendant', back_populates='descendant', cascade="all, delete-orphan")
    descendants  = relationship('Tree', foreign_keys='Tree.rid_ancestor',   back_populates='ancestor',   cascade="all, delete-orphan")

    summary_item = relationship('SummaryItem', back_populates='items')

    project      = relationship('Project',  back_populates='items')
    event        = relationship('Event',    back_populates='items')
    feature      = relationship('Feature',  back_populates='items')
    story        = relationship('Story',    back_populates='items')
    task         = relationship('Task',     back_populates='items')
    bug          = relationship('Bug',      back_populates='items')
    activity     = relationship('Activity', back_populates='items')

    user         = relationship('User', foreign_keys=[rid_users], back_populates='items')
    user_review  = relationship('User', foreign_keys=[rid_users_review], back_populates='items_review')

    __table_args__ = (
        Index('idx_items_01', 'is_deleted', 'type', 'rid'),
        Index('idx_items_02', 'is_deleted', 'rid', 'path_sort', 'priority'),
        Index('idx_items_03', 'is_deleted', 'id_project', 'datetime_entry'),
        Index('idx_items_04', 'is_deleted', 'type', 'state'),
    )
