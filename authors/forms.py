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

    first_name = forms.CharField(
        validators=[lambda value: field_size_correct('First name', value, 4)],  # noqa: E501
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your first name here',
            'class': 'input text-input'
        })
    )

    last_name = forms.CharField(
        validators=[lambda value: field_size_correct('Last name', value, 4)],  # noqa: E501
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your last name here',
            'class': 'input text-input'
        })
    )

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
                '"Password" and "Password2" must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': error,
                'password2': error
            })
