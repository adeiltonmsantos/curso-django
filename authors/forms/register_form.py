from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import (
    edit_attr_widget_field,
    field_size_correct,
    strong_password,
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

    def clean_email(self):
        email = self.cleaned_data.get('email', None)

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'This e-mail is already in use',
                code='invalid'
            )

        return email

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
