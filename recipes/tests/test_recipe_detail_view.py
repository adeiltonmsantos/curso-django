from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_view_recipe_is_correct(self):
        """
        Test if a recipe in databank is loaded correctly in recipe detail view
        """
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_view_recipe_detail_view_returns_404_if_no_recipes_found(self):  # noqa: E501
        """
        Test if template recipe detail returns 404 if a non existing recipe
        is requested
        """
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_correct_recipes(self):
        """
        Test if recipe detail template loads a saved recipe correctly
        """
        neeed_title = 'This is a category test'
        self.make_recipe(title=neeed_title)
        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        content = response.content.decode('utf-8')
        self.assertIn(neeed_title, content)

    def test_recipe_view_recipe_doesnt_loads_not_published_recipes(self):
        """
        Test if recipe detail template doesn't load not published recipe
        """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})
        )
        self.assertEqual(response.status_code, 404)
