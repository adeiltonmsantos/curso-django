from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def edit_attr_widget_field(field, attr_name, attr_val):
    field.widget.attrs[attr_name] = attr_val


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

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
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
        # exclude = ['first_name']
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'The e-mail must be valid.',
        }
        error_messages = {
            'username': {
                'required': 'This field must not be empty',
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
                'class': 'input text-input'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if len(data) < 4:
            raise ValidationError(
                '"First name" field must have more then %(value)s letters',
                code='invalid',
                params={'value': 3}
            )

        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name')

        if len(data) < 4:
            raise ValidationError(
                '"Last name" field must have more then %(value)s letters',
                code='invalid',
                params={'value': 3}
            )

        return data
