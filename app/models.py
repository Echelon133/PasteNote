from sqlalchemy import (Column, String, Text, Bool, DateTime)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Notes(Base):
    __tablename__ = 'notes'
    hash = Column(String(10), primary_key=True)
    title = Column(String())
    expiration = Column(DateTime())
    content = Column(Text())
    expired = Column(Bool())