from django.test import TestCase  # import: ignore
from django.urls import resolve, reverse

from recipes import views


class RecipeViewsTest(TestCase):

    def test_recipe_view_home_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_view_home_statuscode_200_is_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_view_home_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_view_home_template_shows_no_recipe_found_if_no_recipes(self):  # noqa: E501
        response = self.client.get(reverse('recipes:home'))
        info = '<h2>Nenhuma receita encontrada 😢</h2>'
        html_txt = response.content.decode('utf-8')
        self.assertIn(info, html_txt)

    def test_recipe_view_category_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_view_category_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_view_recipes_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_view_recipe_detail_view_returns_404_if_no_recipes_found(self):  # noqa: E501
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)
