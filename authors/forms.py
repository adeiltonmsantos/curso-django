from django.contrib.auth.models import User
from django.forms import ModelForm


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'username': 'Username',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'first_name': 'O nome deve ter pelo menos 4 caracteres'
        }
