from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

import sys
sys.path.append('~/app')

from database import Base


class Task(Base):
    __tablename__ = 'tasks'

    rid              = Column(Integer, primary_key=True)
    rid_items        = Column(Integer, ForeignKey('items.rid'))
    type             = Column(Integer, default=0)
    workload         = Column(Integer, default=0)
    number_completed = Column(Integer, default=0)
    number_total     = Column(Integer, default=0)

    items = relationship('Item', back_populates='task')
