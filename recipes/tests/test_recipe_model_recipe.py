from django.core.exceptions import ValidationError
from parameterized import parameterized  # type: ignore

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_without_defaults(self):
        recipe = Recipe(
            category=self.create_category(name='Test Default Category'),
            author=self.create_author(username='userdefault'),
            title='Recipe title',
            description='Recipe description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe preparation_steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_raise_maxlength_error(self, field, maxlength):
        setattr(self.recipe, field, 'A' * (maxlength + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_without_defaults()
        # recipe.preparation_steps_is_html = True
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Preparation_steps_is_html must be False by default'
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_without_defaults()
        # recipe.is_published = True
        self.assertFalse(
            recipe.is_published,
            msg='is_published must be False by default'
        )
