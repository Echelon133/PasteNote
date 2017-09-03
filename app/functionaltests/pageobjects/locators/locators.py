from selenium.webdriver.common.by import By


class BaseLocators:
    homepage_link = (By.XPATH, '//h1[@class="text-center"]/a')


class HomePageLocators(BaseLocators):
    note_title_field = (By.ID, 'inputTitle')
    note_expiration_field = (By.ID, 'expireIn')
    note_content_field = (By.ID, 'contentText')
    note_save_button = (By.ID, 'button')
    result_box = (By.XPATH, '//*[@class="result-box"]/div[1]')
    url_response = (By.ID, 'noteLink')


class NotePageLocators(BaseLocators):
    note_title = (By.XPATH, '//h4[@class="text-center"]')
    note_content = (By.ID, 'contentText')
    raw_note_link = (By.XPATH, '//a[@class="display-menu-item"][1]')
    download_note_link = (By.XPATH, '//a[@class="display-menu-item"][2]')


class RawNotePageLocators:
    note_content = (By.XPATH, '/html/body/span')


class NotFoundPageLocators(BaseLocators):
    error_number = (By.CLASS_NAME, 'error-number')
    error_text = (By.CLASS_NAME, 'error-text')
    