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
        ('email', 'The e-mail must be valid.'),
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
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'user@email.com',
            'password': 'Str0ngP@ssw0rd1',
            'password2': 'Str0ngP@ssw0rd1'
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'Este campo é obrigatório'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        ...
