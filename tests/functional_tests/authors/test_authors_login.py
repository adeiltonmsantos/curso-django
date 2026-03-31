import pytest
from django.contrib.auth.models import User
from django.urls import reverse

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
        self.sleep(6)

        # User fill fields with username and password
        form = self.get_by_class_name('main-form')
        login = self.get_by_placeholder(form, 'Type your username here')
        password = self.get_by_placeholder(form, 'Type your password here')
        login.send_keys(user.username)
        password.send_keys(passwd)

        # User submit the form
        form.submit()

        # Form is reloaded
        self.sleep(6)

        # Testing...
        self.assertIn(
            f'You are logged in as {user.username}.',
            self.get_by_tag_name('body').text
        )

    def test_login_create_raises_404_if_not_post_method(self):
        # User trys access login page by get method
        complement_url = reverse('authors:login_create')
        self.browser.get(self.live_server_url + complement_url)
        self.sleep()

        # Testing if raises 404 error
        self.assertIn(
            'Not Found',
            self.get_by_tag_name('body').text
        )

    def test_login_form_is_invalid(self):
        # User opens login page
        complement_url = reverse('authors:login_register')
        self.browser.get(self.live_server_url + complement_url)
        self.sleep()

        # User types blank spaces in login and password fields
        form = self.get_by_class_name('main-form')
        self.get_by_placeholder(form, 'Type your username here').send_keys(' ')  # noqa: E501
        self.get_by_placeholder(form, 'Type your password here').send_keys(' ')  # noqa: E501

        form.submit()
        # form = self.get_by_class_name('main-form')
        self.sleep()

        self.assertIn(
            'Invalid username or password',
            self.get_by_tag_name('body').text
        )

    def test_user_tries_login_with_invalid_credentials(self):
        # User opens login page
        complement_url = reverse('authors:login_register')
        self.browser.get(self.live_server_url + complement_url)
        self.sleep()

        # User types login and password of false user
        form = self.get_by_class_name('main-form')
        self.get_by_placeholder(form, 'Type your username here').send_keys('myUser')  # noqa: E501
        self.get_by_placeholder(form, 'Type your password here').send_keys('@MyPassword')  # noqa: E501

        form.submit()
        form = self.get_by_class_name('main-form')
        self.sleep()

        self.assertIn(
            'Invalid credentials',
            self.get_by_tag_name('body').text
        )
