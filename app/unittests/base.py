import unittest
import uuid
import random


class NoteAppTestCase(unittest.TestCase):

    @staticmethod
    def get_random_string(length=None):
        '''
        If no length provided, give strings
        that have from 1 to 31 chars
        '''
        string = uuid.uuid4().hex
        if length is None:
            length = random.randint(1, 31)
        return string[:length]
    
    def get_dates_delta(self, date1, date2):
        return date1 - date2