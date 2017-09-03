from ..exceptions import (InvalidExpirationFieldValue, ExpirationFieldEmpty, 
                          CannotCreateEmptyNote)
from .base import NoteAppTestCase
from ..models import Notes
from ..views import app
import datetime
import random


class ModelsUnittest(NoteAppTestCase):
    
    def setUp(self):
        self.note = Notes()
    
    def test_set_hash_is_correct(self):
        self.note.set_hash()

        # Hash should be alphanumeric
        self.assertTrue(self.note.hash.isalnum())

        # Hash should be exactly 10 characters long
        self.assertEqual(len(self.note.hash), 10)

    def test_set_title_is_correct(self):
        # Title should be 'Untitled' when title argument is empty
        self.note.set_title('')
        self.assertEqual(self.note.title, 'Untitled')

        # set_title shortens titles longer than 80 chars
        my_title = 'Test' * 21 # 84 chars
        self.note.set_title(my_title)
        self.assertEqual(len(self.note.title), 80)

        # Check if regular titles are set properly
        titles = ['Test title one', 'Other title']
        for title in titles:
            self.note.set_title(title)
            self.assertEqual(self.note.title, title)

    def test_set_expiration_is_correct(self):
        # Never expire
        self.note.set_expiration(5)
        self.assertEqual(self.note.expiration, datetime.datetime.max)

        # Expire in 7 days
        self.note.set_expiration(4)
        now = datetime.datetime.now()
        expiration = self.note.expiration

        date_delta = self.get_dates_delta(expiration, now)
        date_delta_seconds = date_delta.total_seconds()
        week_seconds = datetime.timedelta(hours=24*7).total_seconds()
        self.assertAlmostEqual(date_delta_seconds, week_seconds, places=2)

        # Expire in a day
        self.note.set_expiration(3)
        now = datetime.datetime.now()
        expiration = self.note.expiration

        date_delta = self.get_dates_delta(expiration, now)
        date_delta_seconds = date_delta.total_seconds()
        week_seconds = datetime.timedelta(hours=24).total_seconds()
        self.assertAlmostEqual(date_delta_seconds, week_seconds, places=4)

        # Give random big number as an argument
        random_number = random.randint(100, 10000)
        with self.assertRaises(InvalidExpirationFieldValue):
            self.note.set_expiration(random_number)

        # Give some random string as an argument
        random_string = self.get_random_string()
        with self.assertRaises(InvalidExpirationFieldValue):
            self.note.set_expiration(random_string)

        # Give no arguments
        with self.assertRaises(ExpirationFieldEmpty):
            self.note.set_expiration()

    def test_set_content_is_correct(self):
        # Empty content should not be allowed
        with self.assertRaises(CannotCreateEmptyNote):
            self.note.set_content()

        # Set content to some random string 10 times
        for x in range(10):
            random_string = self.get_random_string() * 50
            self.note.set_content(random_string)
            self.assertEqual(random_string, self.note.content)

    def test_is_expired_is_correct(self):
        # Every time the result should be False for every new note
        for x in range(20):
            expiration_mode = random.randint(0, 5)
            self.note.set_expiration(expiration_mode)
            self.assertFalse(self.note.is_expired())

    def test_serialize_is_correct(self):
        for x in range(10):
            # Set values needed for serializing a note
            self.note.set_hash()
            hash_ = self.note.hash 

            title = self.get_random_string()
            self.note.set_title(title)

            expiration_mode = random.randint(0, 5)
            self.note.set_expiration(expiration_mode)

            content = self.get_random_string() * 50
            self.note.set_content(content)

            # Serialize a note
            with app.test_request_context():
                serialized = self.note.serialize

            # Assert that passed values are the same after serialization
            self.assertIn(hash_, serialized['url'])
            self.assertEqual(title, serialized['title'])
            self.assertEqual(content, serialized['content'])

            
