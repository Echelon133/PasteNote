from .pageobjects.pages import HomePage, NotePage, RawNotePage, NotFoundPage
from selenium import webdriver
import unittest


class FunctionalTest(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()


class NoteFunctionalTest(FunctionalTest):
    
    def setUp(self):
        super(NoteFunctionalTest, self).setUp()
        self.driver.get('http://localhost:5000')
        self.driver.implicitly_wait(5)

    def test_add_note_check_result(self):
        self.homepage_obj = HomePage(self.driver)

        title = 'Test title'
        expire_in = 'One hour'
        content = 'Test123\n' * 50

        # Set full note data and save it
        self.homepage_obj.set_note_title(title)
        self.homepage_obj.set_note_expiration(expire_in)
        self.homepage_obj.set_note_content(content)
        self.homepage_obj.save_note()
        
        # Wait for response from server, then copy link and visit it
        self.driver.implicitly_wait(5)
        self.notepage_obj = self.homepage_obj.visit_new_note_page()

        # Compare entered data with data received
        self.driver.implicitly_wait(5)
        received_title = self.notepage_obj.get_note_title()
        received_content = self.notepage_obj.get_note_content()
        # When displayed, content is wrapped by spaces
        self.assertEqual(received_title.strip(), title.strip())
        self.assertEqual(received_content.strip(), content.strip())

        # Check raw note link
        self.raw_notepage_obj = self.notepage_obj.visit_raw_note_page()
        received_raw_content = self.raw_notepage_obj.get_note_content()
        # Compare entered data with raw text received
        self.assertEqual(received_raw_content.strip(), content.strip())

    def test_add_note_without_content(self):
        self.homepage_obj = HomePage(self.driver)

        expire_in = 'Two hours'
        self.homepage_obj.set_note_expiration(expire_in)

        # Try to save note without setting the content field
        # so that the alert appears
        self.homepage_obj.save_note()
        alert_text = self.homepage_obj.get_alert_text()
        self.assertEqual(alert_text, 'Content field cannot be empty')

    def test_check_invalid_note_url(self):
        self.driver.get(self.driver.current_url + '/notes/test')
        self.error_page = NotFoundPage(self.driver)

        error_number = self.error_page.get_error_number()
        error_text = self.error_page.get_error_text()

        self.assertEqual(error_number, '404')
        self.assertEqual(error_text, 'Page Not Found')