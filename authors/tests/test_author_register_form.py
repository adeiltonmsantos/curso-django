from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized  # type: ignore

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Your username here'),
        ('email', 'Your e-mail here'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Your password here'),
        ('password2', 'Repeat your password here')
    ])
    def test_fields_placeholder(self, field_name, placeholder):
        form = RegisterForm()
        current_placeholder = form.fields[field_name].widget.attrs['placeholder']  # noqa: E501
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('password',
         ('Password must have at least one uppercase letter, '
          'one lowercase letter and one number. The length should be '
          'at least 8 characters.')
         ),
        ('email', 'The e-mail must be valid'),
    ])
    def test_fields_help_texts(self, field_name, help_text):
        form = RegisterForm()
        current_help_text = form.fields[field_name].help_text  # noqa: E501
        self.assertEqual(current_help_text, help_text)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password 2'),
    ])
    def test_fields_labels(self, field_name, label):
        form = RegisterForm()
        current_label = form.fields[field_name].label
        self.assertEqual(current_label, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.form_data = {}
        return super().setUp()

    @parameterized.expand([
        ('username', 'Username must not be empty'),
        ('first_name', 'First name must not be empty'),
        ('last_name', 'Last name must not be empty'),
        ('email', 'E-mail must not be empty'),
        ('password', 'Password must not be empty'),
        ('password2', 'Password 2 must not be empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(
            msg,
            response.content.decode('utf-8'),
            msg=f'For "{field}" field, error message should be "{msg}"'
        )

    def test_first_name_field_min_length(self):
        self.form_data['first_name'] = 'a' * 2
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(
            'First name must have at least 4 characters',
            response.content.decode('utf-8'),
            msg='"Fist name" field must have at least 4 characters'
        )

    def test_first_name_field_max_length(self):
        self.form_data['first_name'] = 'a' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(
            'Maximum value of characters for First name is 150',
            response.content.decode('utf-8'),
            msg='"Fist name" field must have less then 151 characters'
        )

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'ab12'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )

        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password and Password2 must be equal'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc1235'

        url = reverse('authors:create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_register_form_valid_data(self):
        self.form_data = {
            'first_name': 'José',
            'last_name': 'Silva',
            'username': 'jsilva',
            'email': 'jsilva@email.com',
            'password': '@Jsabc123',
            'password2': '@Jsabc123'
        }

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(
            'Your user is created, please log in.',
            response.content.decode('utf-8')
        )

    def test_email_field_must_be_unique(self):
        self.form_data = {
            'first_name': 'José',
            'last_name': 'Silva',
            'username': 'jsilva',
            'email': 'jsilva@email.com',
            'password': '@Jsabc123',
            'password2': '@Jsabc123'
        }

        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'This e-mail is already in use'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email'))
