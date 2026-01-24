from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category(name='Category Test')
        return super().setUp()

    def test_recipe_category_model_string_representation(self):
        needed = 'Category Test'
        self.category.name = 'Category Test'
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            str(self.category),
            needed,
            msg=f'Category string representation must be "{needed}"'
            f' but "{self.category.name}" was received'
        )

    def test_recipe_category_model_name_maxlength_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(
            ValidationError,
            msg='Category name field maxlength should be 65'
        ):
            self.category.full_clean()
