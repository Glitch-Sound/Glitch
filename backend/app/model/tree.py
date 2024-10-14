from sqlalchemy import ForeignKey, Column, Integer
from sqlalchemy.orm import relationship

import sys
sys.path.append('~/app')

from database import Base


class Tree(Base):
    __tablename__ = 'trees'

    rid_ancestor   = Column(Integer, ForeignKey('items.rid'), primary_key=True)
    rid_descendant = Column(Integer, ForeignKey('items.rid'), primary_key=True)
    type           = Column(Integer, default=0)

    ancestor   = relationship('Item', foreign_keys=[rid_ancestor],   back_populates='descendants')
    descendant = relationship('Item', foreign_keys=[rid_descendant], back_populates='ancestors')
