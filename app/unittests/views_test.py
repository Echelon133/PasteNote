from ..views import app
from .base import NoteAppTestCase
import random
import flask
import json


def get_mock_note_data(title=None, expiration=None, content=None):
    if title is None:
        title = NoteAppTestCase.get_random_string()
    if expiration is None:
        expiration = random.randint(0, 5)
    if content is None:
        content = NoteAppTestCase.get_random_string()

    return (title, expiration, content)


class ViewsUnittest(NoteAppTestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home_page_renders_correctly(self):
        rs = self.app.get('/')
        
        # Check if status is 200 OK and page title is correct
        self.assertEqual(rs.status, '200 OK')
        self.assertIn(b'<title>PasteNote</title>', rs.data)

        # Home page contains the form used for adding notes
        self.assertIn(b'<form id="main">', rs.data)

    def test_invalid_hash_gives_404(self):
        for l in range(1, 9):
            hash_ = self.get_random_string(length=l)
            rs = self.app.get('/notes/' + hash_)

            # Check if 404 page renders
            self.assertIn(b'<title>404</title>', rs.data)
            self.assertIn(b'<p class="text-center error-text">Page Not Found</p>', rs.data)

    def test_add_note_and_check_correctness(self):
        title, exp, content = get_mock_note_data()
        
        rs = self.app.post('/notes', data=dict(title=title, 
                                               expiration=exp,
                                               content=content))
        json_res = json.loads(rs.data.decode())['note']
        recv_title = json_res['title']
        recv_content = json_res['content']

        # Compare sent data with received json response
        self.assertEqual(title, recv_title)
        self.assertEqual(content, recv_content)

    def test_add_note_with_invalid_expiration_field(self):
        # Every value not in 0..5 range is invalid
        expiration = random.randint(6, 1000)
        title, exp, content = get_mock_note_data(expiration=expiration)

        rs = self.app.post('/notes', data=dict(title=title,
                                               expiration=exp,
                                               content=content))
        json_res = json.loads(rs.data.decode())
        recv_error = json_res['error']
        self.assertEqual(recv_error, 'EXPIRATION_FIELD_INVALID')

    def test_add_note_with_empty_expiration_field(self):
        title, exp, content = get_mock_note_data()

        rs = self.app.post('/notes', data=dict(title=title,
                                               content=content))
        json_res = json.loads(rs.data.decode())
        recv_error = json_res['error']
        self.assertEqual(recv_error, 'EXPIRATION_FIELD_EMPTY')
        
    def test_add_note_with_empty_content_field(self):
        title, exp, content = get_mock_note_data()

        rs = self.app.post('/notes', data=dict(title=title,
                                               expiration=exp))

        json_res = json.loads(rs.data.decode())
        recv_error = json_res['error']
        self.assertEqual(recv_error, 'CONTENT_FIELD_EMPTY')

    def test_add_note_and_check_rendered_template(self):
        title, exp, content = get_mock_note_data()

        # Create a note with random data
        rs = self.app.post('/notes', data=dict(title=title,
                                               expiration=exp,
                                               content=content))
        json_res = json.loads(rs.data.decode())['note']

        # Read in data from response
        hash_ = json_res['hash']
        title = json_res['title']
        content = json_res['content']

        # Check previously created note 
        rs = self.app.get('/notes/' + hash_)

        # Make sure everything was saved properly
        title_html = '<title> {} </title>'.format(title)
        self.assertIn(title_html.encode(), rs.data)
        content_html = '<p class="note-content" id="contentText"> {} </p>'.format(content)
        self.assertIn(content_html.encode(), rs.data)

        # Check whether displaying a note in a raw style works
        raw_url = '/notes/' + hash_ + '?action=raw'
        rs = self.app.get(raw_url)
        # Template for raw display has styles embedded in HTML
        self.assertIn(b'word-wrap: break-word', rs.data)

        


    
