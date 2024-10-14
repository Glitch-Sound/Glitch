from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import sys
sys.path.append('~/app')

from database import Base


class Story(Base):
    __tablename__ = 'stories'

    rid            = Column(Integer, primary_key=True)
    rid_items      = Column(Integer, ForeignKey('items.rid'))
    datetime_start = Column(String,  default='')
    datetime_end   = Column(String,  default='')

    items = relationship('Item', back_populates='story')
