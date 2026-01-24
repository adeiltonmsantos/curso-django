from django.core.exceptions import ValidationError
from parameterized import parameterized  # type: ignore

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_without_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
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

    @parameterized.expand([
        ('is_published',),
        ('preparation_steps_is_html',)
    ])
    def test_recipe_default_fields_are_false_by_default(self, field):
        recipe = self.make_recipe_without_defaults()
        # setattr(recipe, field, True)
        self.assertFalse(
            getattr(recipe, field),
            msg=f'{field} must be False by default'
        )

    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe),
            needed,
            msg=f'Recipe string must be "{needed}"'
            f' but "{self.recipe.title}" was found'
        )
