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

    def form_field_test_with_callback(self, callback):
        # Opening browser in form template...
        self.browser.get(self.live_server_url + '/authors/register/')

        # Selecting form by fullXpath
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')

        # Filling fields form with valid data
        self.fill_form_dummy_data(form)

        # Filling e-mail field with valid data
        form.find_element(
            By.NAME,
            'email'
        ).send_keys('dummy@email.com')

        # Calling callback function to test the interest field
        callback(form)

    def test_empty_first_name_error_message(self):
        def callback(form):
            # Selecting the interest field
            first_name_field = self.get_by_placeholder(form, 'Ex.: John')

            # Filling the field with invalid characters
            first_name_field.send_keys('   ')

            # Submiting the form with ENTER in field
            first_name_field.send_keys(Keys.ENTER)

            # Selecting form after submit
            form = self.get_by_fullxpath('/html/body/main/div[3]/form')

            # Testing error message
            self.assertIn('First name must not be empty', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            # Selecting the interest field
            last_name_field = self.get_by_placeholder(form, 'Ex.: Doe')

            # Filling the field with invalid characters
            last_name_field.send_keys('   ')

            # Submiting the form with ENTER in field
            last_name_field.send_keys(Keys.ENTER)

            # Selecting form after submit
            form = self.get_by_fullxpath('/html/body/main/div[3]/form')

            # Testing error message
            self.assertIn('Last name must not be empty', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            # Selecting the interest field
            username_field = self.get_by_placeholder(
                form, 'Your username here')

            # Filling the field with invalid characters
            username_field.send_keys('   ')

            # Submiting the form with ENTER in field
            username_field.send_keys(Keys.ENTER)

            # Selecting form after submit
            form = self.get_by_fullxpath('/html/body/main/div[3]/form')

            # Testing error message
            self.assertIn('Username must not be empty', form.text)

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            # Selecting the interest field
            email_field = self.get_by_placeholder(
                form, 'Your e-mail here')

            # Filling the field with invalid characters
            email_field.send_keys('email@invalid')

            # Submiting the form with ENTER in field
            email_field.send_keys(Keys.ENTER)

            # Selecting form after submit
            form = self.get_by_fullxpath('/html/body/main/div[3]/form')

            # Testing error message
            self.assertIn('The e-mail must be valid', form.text)

        self.form_field_test_with_callback(callback)
