import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def edit_attr_widget_field(field, attr_name, attr_val):
    field.widget.attrs[attr_name] = attr_val


def field_size_correct(field_name_print, field_cleaned_data, field_size):  # noqa: E501
    """
    field_size_correct(): if field size < 'field_size' a ValidationError is raised
        - field_name_print: field name to show in message
        - field_cleaned_data: value of field from self.cleaned_data
        - field_size: if filed size is smaller then field_size an error raises # noqa: E501
    """
    if len(field_cleaned_data) < field_size:
        raise ValidationError(
            f'"{field_name_print}" field must have more then %(value)s letters',  # noqa: E501
            code='invalid',
            params={'value': field_size}
        )


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
            code='invalid'
        )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        edit_attr_widget_field(
            self.fields['username'], 'placeholder', 'Your username here')
        edit_attr_widget_field(
            self.fields['email'], 'placeholder', 'Your e-mail here')
        edit_attr_widget_field(
            self.fields['first_name'], 'placeholder', 'Ex.: John')
        edit_attr_widget_field(
            self.fields['last_name'], 'placeholder', 'Ex.: Doe')
        edit_attr_widget_field(
            self.fields['password'], 'placeholder', 'Your password here')
        edit_attr_widget_field(
            self.fields['password2'], 'placeholder', 'Repeat your password here')  # noqa: E501

    first_name = forms.CharField(
        label='First name',
        validators=[lambda value: field_size_correct('First name', value, 4)],  # noqa: E501
        widget=forms.TextInput(attrs={
            'class': 'input text-input'
        }),
        error_messages={
            'required': 'First name must not be empty',
            'min_length': 'First name must have at least 4 characters',
            'max_length': 'Maximum value of characters for First name is 150',
        },
        min_length=3,
        max_length=150
    )

    last_name = forms.CharField(
        label='Last name',
        validators=[lambda value: field_size_correct('Last name', value, 4)],  # noqa: E501
        widget=forms.TextInput(attrs={
            'class': 'input text-input'
        }),
        error_messages={'required': 'Last name must not be empty'}
    )

    email = forms.EmailField(
        label='E-mail',
        error_messages={'required': 'E-mail must not be empty'},
        help_text='The e-mail must be valid'
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        error_messages={'required': 'Password must not be empty'},
        validators=[strong_password]
    )
    password2 = forms.CharField(
        label='Password 2',
        widget=forms.PasswordInput(),
        error_messages={'required': 'Password 2 must not be empty'}
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        labels = {
            'username': 'Username',
            'email': 'E-mail',
        }
        error_messages = {
            'username': {
                'required': 'Username must not be empty',
            },
        }
        widgets = {
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }

    def clean(self):
        cleaned_data = super().clean()

        pswd = cleaned_data.get('password')
        pswd2 = cleaned_data.get('password2')

        if pswd != pswd2:
            error = ValidationError(
                'Password and Password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': error,
                'password2': error
            })
