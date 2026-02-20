from django import forms

from utils.django_forms import edit_attr_widget_field


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        edit_attr_widget_field(
            self.fields['username'], 'placeholder', 'Type your username here')
        edit_attr_widget_field(
            self.fields['password'], 'placeholder', 'Type your password here')

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
