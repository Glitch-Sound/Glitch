from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

import sys
sys.path.append('~/app')

from database import Base


class Feature(Base):
    __tablename__ = 'features'

    rid       = Column(Integer, primary_key=True)
    rid_items = Column(Integer, ForeignKey('items.rid'))

    items = relationship('Item', back_populates='feature')
