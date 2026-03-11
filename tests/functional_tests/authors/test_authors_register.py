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

<<<<<<< HEAD
    def get_by_fullxpath(self, fullxpath):
        return self.browser.find_element(
            By.XPATH,
            fullxpath
        )

    def form_field_test_with_callback(self, callback):
        # Opening browser in form template...
        self.browser.get(self.live_server_url + '/authors/register/')

        # Selecting form by fullXpath
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')

        # Filling fields form with valid data
        self.fill_form_dummy_data(form)

        # Filling e-mail field with valid data
=======
    def test_empty_first_name_error_message(self):
        # Opening browser in form route
        self.browser.get(self.live_server_url + '/authors/register/')

        # Selecting form in browser
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')

        # Filling form fields
        self.fill_form_dummy_data(form)

        # Selecting e-mail field to fill with valid characters
>>>>>>> 31e502c26a41c6422e3c8c9226bc2c7bc66d46d2
        form.find_element(
            By.NAME,
            'email'
        ).send_keys('dummy@email.com')

<<<<<<< HEAD
        # Calling callback function to test the interest field
        callback(form)

    def test_empty_first_name_error_message(self):
        def callback(form):
            # Selecting the interest field
            first_name_field = self.get_by_placeholder(form, 'Ex.: John')

            # Filling the field with invalid data
            first_name_field.send_keys('   ')

            # Submiting the form with ENTER in field
            first_name_field.send_keys(Keys.ENTER)

            # Selecting form after submit
            form = self.get_by_fullxpath('/html/body/main/div[3]/form')

            # Testing error message
            self.assertIn('First name must not be empty', form.text)

        self.form_field_test_with_callback(callback)
=======
        # Selecting desired field (first_name)
        first_name_field = self.get_by_placeholder(form, 'Ex.: John')

        # Leaving first_name empty to invalidate form
        first_name_field.send_keys('    ')

        # Submiting form
        first_name_field.send_keys(Keys.ENTER)

        # Selecting form in browser again after page reloading
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')

        self.assertIn('First name must not be empty', form.text)
>>>>>>> 31e502c26a41c6422e3c8c9226bc2c7bc66d46d2
