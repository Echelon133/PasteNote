from .locators.locators import (HomePageLocators, NotePageLocators, 
                               RawNotePageLocators, NotFoundPageLocators)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from contextlib import contextmanager
from selenium import webdriver


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def get_page_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url


class HomePage(BasePage):

    def set_note_title(self, text):
        field = self.find_element(*HomePageLocators.note_title_field)
        field.send_keys(text)

    def set_note_expiration(self, expiration=None):
        select = Select(self.find_element(*HomePageLocators.note_expiration_field))
        modes = {'one hour': 0, 'six hours': 1,
                 'twelve hours': 2, 'one day': 3,
                 'one week': 4, 'never': 5}
        if expiration is None:
            # set expiration to 'never' by default
            mode = modes['never']
        else:
            try:
                mode = modes[expiration.lower()]
            except KeyError:
                # on key error set to 'never'
                mode = modes['never']
            else:
                select.select_by_value(str(mode))
    
    def set_note_content(self, text):
        field = self.find_element(*HomePageLocators.note_content_field)
        field.send_keys(text)

    def save_note(self):
        button = self.find_element(*HomePageLocators.note_save_button)
        button.click()

    @contextmanager
    def wait_for_result_box(self):
        yield WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(HomePageLocators.result_box)
        )

    @contextmanager
    def wait_for_alert(self):
        yield WebDriverWait(self.driver, 10).until(
            EC.alert_is_present()
        )

    def get_alert_text(self):
        with self.wait_for_alert():
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text

    def visit_new_note_page(self):
        with self.wait_for_result_box():
            url_field = self.find_element(*HomePageLocators.url_response)
        note_page_url = url_field.get_attribute('value')
        self.driver.get(note_page_url)
        return NotePage(self.driver)
        

class NotePage(BasePage):

    def get_note_title(self):
        note_title = self.find_element(*NotePageLocators.note_title)
        return note_title.text

    def get_note_content(self):
        note_content = self.find_element(*NotePageLocators.note_content)
        return note_content.text

    def visit_raw_note_page(self):
        raw_link = self.find_element(*NotePageLocators.raw_note_link)
        raw_link.click()
        return RawNotePage(self.driver)


class RawNotePage(BasePage):
    
    def get_note_content(self):
        note_content = self.find_element(*RawNotePageLocators.note_content)
        return note_content.text


class NotFoundPage(BasePage):
    
    def get_error_number(self):
        error_number = self.find_element(*NotFoundPageLocators.error_number)
        return error_number.text

    def get_error_text(self):
        error_text = self.find_element(*NotFoundPageLocators.error_text)
        return error_text.text

