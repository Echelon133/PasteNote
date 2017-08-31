from .exceptions import CannotCreateEmptyNote, InvalidExpirationFieldValue, ExpirationFieldEmpty
from sqlalchemy import (Column, String, Text, Boolean, DateTime)
from sqlalchemy.ext.declarative import declarative_base
from .helper_functions import get_hash
from sqlalchemy import create_engine
from flask import url_for
import datetime


Base = declarative_base()


class Notes(Base):
    __tablename__ = 'notes'
    hash = Column(String(10), primary_key=True)
    title = Column(String(80))
    expiration = Column(DateTime())
    content = Column(Text())

    def set_hash(self):
        self.hash = get_hash()

    def set_title(self, title=''):
        title = str(title)[:80]
        if title:
            self.title = title
        else:
            self.title = 'Untitled'

    def set_expiration(self, num=None):
        self.HOURS = {0: (1, 'One hour'), 
                      1: (6, 'Six hours'),
                      2: (12, 'Twelve hours'),
                      3: (24, 'One day'),
                      4: (24 * 7, 'One week'), 
                      5: (-1, 'Never')}
        try:
            num = int(num)
        except ValueError:
            raise InvalidExpirationFieldValue()
        except TypeError:
            raise ExpirationFieldEmpty()

        if num == 5:
            # Set expiration date to the max value possible
            self.expiration = datetime.datetime.max
        else:
            now = datetime.datetime.now()

            try:
                additional_hours = self.HOURS[num][0]
            except KeyError:
                raise InvalidExpirationFieldValue()
            else:
                expiration = now + datetime.timedelta(hours=additional_hours)
                self.expiration = expiration

    def set_content(self, content=None):
        if content:
            self.content = content
        else:
            raise CannotCreateEmptyNote()

    def is_expired(self):
        if self.expiration < datetime.datetime.now():
            return True
        else:
            return False
        
    @property
    def serialize(self):
        full_url = url_for('get_note', _external=True, hash=self.hash)
        return {'hash': self.hash, 'url': full_url, 'title': self.title, 'content': self.content}


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)