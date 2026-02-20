import re

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
