from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

import sys
sys.path.append('~/app')

from database import Base


class Bug(Base):
    __tablename__ = 'bugs'

    rid       = Column(Integer, primary_key=True)
    rid_items = Column(Integer, ForeignKey('items.rid'))
    workload  = Column(Integer, default=0)

    items = relationship('Item', back_populates='bug')
