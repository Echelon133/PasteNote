from exceptions import CannotCreateEmptyNote, InvalidExpirationFieldValue
from sqlalchemy import (Column, String, Text, Bool, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from helper_functions import get_hash
from sqlalchemy import create_engine
import datetime


Base = declarative_base()


class Notes(Base):
    __tablename__ = 'notes'
    hash = Column(String(10), primary_key=True)
    title = Column(String())
    expiration = Column(DateTime())
    content = Column(Text())
    expired = Column(Bool())

    def set_hash(self):
        self.hash = get_hash()

    def set_title(self, title):
        if title:
            self.title = title
        else:
            self.title = 'Untitled'

    def set_expiration(self, num):
        self.HOURS = {0: (1, 'One hour'), 
                      1: (6, 'Six hours'),
                      2: (12, 'Twelve hours'),
                      3: (24, 'One day'),
                      4: (24 * 7, 'One week'), 
                      5: (-1, 'Never')}
        
        now = datetime.datetime.now()

        try:
            additional_hours = self.HOURS[num][0]
        except KeyError:
            raise InvalidExpirationFieldValue
        else:
            expiration = now + datetime.timedelta(hours=additional_hours)
            self.expiration = expiration

    def set_content(self, content):
        if content:
            self.content = content
        else:
            raise CannotCreateEmptyNote()

    def mark_as_expired(self):
        '''
        Set note status to expired, so it is no longer displayed.
        '''
        self.expired = True

    def get_expiration_as_text(self, num):
        return self.HOURS[num][1]
        
    @property
    def serialize(self):
        return {'hash': self.hash, 'title': self.title, 'content': self.content}


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)