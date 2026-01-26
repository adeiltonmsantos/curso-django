from django.test import TestCase  # import: ignore
from django.urls import reverse  # import: ignore


class RecipeURLsTest(TestCase):

    def test_recipe_url_home_is_correct(self):
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_url_category_is_correct(self, id=1):
        url = reverse('recipes:category', kwargs={'category_id': id})
        self.assertEqual(url, f'/recipes/category/{id}/')

    def test_recipe_url_recipe_is_correct(self, id=1):
        url = reverse('recipes:recipe', kwargs={'id': id})
        self.assertEqual(url, f'/recipes/{id}/')

    def test_recipe_url_search_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')
