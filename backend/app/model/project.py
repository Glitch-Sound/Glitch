from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Project(Base):
    __tablename__ = 'projects'

    rid            = Column(Integer, primary_key=True)
    rid_items      = Column(Integer, ForeignKey('items.rid'))
    datetime_start = Column(String,  default='')
    datetime_end   = Column(String,  default='')

    items  = relationship('Item',   back_populates='project')
    member = relationship('Member', back_populates='projects')
