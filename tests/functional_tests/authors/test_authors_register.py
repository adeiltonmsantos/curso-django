from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseFunctionalTest


class AuthorsRegisterFunctionalTest(AuthorsBaseFunctionalTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def get_by_fullxpath(self, xpath):
        return self.browser.find_element(
            By.XPATH,
            xpath
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(
            By.TAG_NAME,
            'input'
        )
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def test_empty_first_name_error_message(self):
        # Opening browser in form route
        self.browser.get(self.live_server_url + '/authors/register/')

        # Selecting form in browser
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')

        # Filling form fields
        self.fill_form_dummy_data(form)

        # Selecting e-mail field to fill with valid characters
        form.find_element(
            By.NAME,
            'email'
        ).send_keys('dummy@email.com')

        # Selecting desired field (first_name)
        first_name_field = self.get_by_placeholder(form, 'Ex.: John')

        # Leaving first_name empty to invalidate form
        first_name_field.send_keys('    ')

        # Submiting form
        first_name_field.send_keys(Keys.ENTER)

        # Selecting form in browser again after page reloading
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')

        self.assertIn('First name must not be empty', form.text)
