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
        self.sleep()

        # User fill fields with username and password
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        login = self.get_by_placeholder(form, 'Type your username here')
        password = self.get_by_placeholder(form, 'Type your password here')
        login.send_keys(user.username)
        password.send_keys(passwd)

        # User submit the form
        form.submit()

        # Form is reloaded
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.sleep()

        # Testing...
        self.assertIn(
            f'You are logged in as {user.username}.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_post_method(self):
        # User trys access login page by get method
        complement_url = reverse('authors:login_create')
        self.browser.get(self.live_server_url + complement_url)
        self.sleep()

        # Testing if raises 404 error
        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_view_if_user_is_not_authenticated_with_none_data(self):
        # User opend login page
        complement_url = reverse('authors:login_register')
        self.browser.get(self.live_server_url + complement_url)
        self.sleep()

        # User types blank spaces in login and password fields
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.get_by_placeholder(form, 'Type your username here').send_keys('   ')  # noqa: E501
        self.get_by_placeholder(form, 'Type your password here').send_keys('   ')  # noqa: E501

        form.submit()
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.sleep()

        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )