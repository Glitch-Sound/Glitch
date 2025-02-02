from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import Base


class Member(Base):
    __tablename__ = 'members'

    rid            = Column(Integer, primary_key=True)
    rid_projects   = Column(Integer, ForeignKey('projects.rid'))
    rid_users      = Column(Integer, ForeignKey('users.rid'))

    projects = relationship('Project', back_populates='member')
    user     = relationship('User',    back_populates='member')
