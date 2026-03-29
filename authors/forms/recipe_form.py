from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import edit_attr_widget_field
from utils.strings import is_positive


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        edit_attr_widget_field(
            self.fields.get('preparation_steps'),
            'class',
            'span-2'
        )
        edit_attr_widget_field(
            self.fields.get('cover'),
            'class',
            'span-2'
        )

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', \
            'servings_unit', 'preparation_steps', 'cover'

        widgets = {
            'cover': forms.FileInput(
                attrs={'class': 'span-2'}
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pratos', 'Pratos'),
                    ('Fatias', 'Fatias'),
                    ('Unidades', 'Unidades'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean(self):
        super_clean = super().clean()
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if title == description:
            self._my_errors['title'].append(
                'Title can not be equall Description')
            self._my_errors['description'].append(
                'Description can not be equall Title')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            self._my_errors['title'].append('Title must have at least 5 chars')
        return title

    def clean_preparation_time(self):
        value = self.cleaned_data.get('preparation_time')
        if not is_positive(value):
            self._my_errors['preparation_time'].append(
                'Preparation Time must be a positive number')
        return value

    def clean_servings(self):
        value = self.cleaned_data.get('servings')
        if not is_positive(value):
            self._my_errors['servings'].append(
                'Servings must be a positive number')
        return value
