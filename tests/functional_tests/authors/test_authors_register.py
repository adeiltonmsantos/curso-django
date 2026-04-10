import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseFunctionalTest


@pytest.mark.functional_test
class AuthorsRegisterFunctionalTest(AuthorsBaseFunctionalTest):
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
            self.sleep()

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
            self.sleep()

            # Selecting form after submit
            form = self.get_by_fullxpath('/html/body/main/div[3]/form')
            self.sleep(7)

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

    def test_passwords_do_not_match(self):
        def callback(form):
            # Selecting the first interest field
            password1 = self.get_by_placeholder(
                form, 'Your password here')

            # Selecting the second interest field
            password2 = self.get_by_placeholder(
                form, 'Repeat your password here')

            # Filling the password1 field
            password1.send_keys('@Abcd1234')

            # Filling the password2 field
            password2.send_keys('@Abcd12345')

            # Submiting the form with ENTER in field
            password2.send_keys(Keys.ENTER)

            # Selecting form after submit
            form = self.get_by_fullxpath('/html/body/main/div[3]/form')

            # Testing error message
            self.assertIn('Password and Password2 must be equal', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        # Opening browser in user register form template
        self.browser.get(self.live_server_url + '/authors/register')
        self.sleep()

        # Selecting the form
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')

        # Filling first_name field
        self.get_by_placeholder(form,
                                'Ex.: John').send_keys('FirstName')

        # Filling last_name field
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('LastName')

        # Filling username field
        self.get_by_placeholder(form,
                                'Your username here').send_keys('UserName')

        # Filling e-mail field
        self.get_by_placeholder(form,
                                'Your e-mail here').send_keys('user@user.com')

        # Filling password field
        self.get_by_placeholder(form,
                                'Your password here').send_keys('@UserName123')

        # Filling password2 field
        self.get_by_placeholder(
            form,
            'Repeat your password here').send_keys('@UserName123')

        # Submiting the form
        form.submit()
        self.sleep()

        # Form updated
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')
        self.sleep()

        # Testing success flash message
        self.assertIn(
            'Your user is created, please log in.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
