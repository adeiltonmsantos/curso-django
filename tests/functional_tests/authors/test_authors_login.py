import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseFunctionalTest


@pytest.mark.functional_test
class AuthorsLoginFunctionalTest(AuthorsBaseFunctionalTest):
    def test_user_valid_data_can_login_successfully(self):
        passwd = 'abc123'
        user = User.objects.create_user(
            username='Username',
            password=passwd
        )

        # User opens browser in login page
        complement_url = reverse('authors:login_register')
        self.browser.get(self.live_server_url + complement_url)

        # User fill fields with username and password
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')
        login = self.get_by_placeholder(form, 'Type your username here')
        password = self.get_by_placeholder(form, 'Type your password here')
        login.send_keys(user.username)
        password.send_keys(passwd)

        # User submit the form
        form.submit()

        # Form is reloaded
        form = self.get_by_fullxpath('/html/body/main/div[3]/form')

        # Testing...
        self.assertIn(
            'You are logged in as Username.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        # User sees success flash message
        # form = self.get_by_fullxpath('/html/body/main/div[3]/form')
