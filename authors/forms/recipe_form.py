from django import forms

from recipes.models import Recipe
from utils.django_forms import edit_attr_widget_field


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
