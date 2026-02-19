from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

    def test_recipe_view_home_is_correct(self):
        """
        Test if view function for home is correct
        """
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_view_home_statuscode_200_is_ok(self):
        """
        Test if status code of view function for home is 200
        """
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_view_home_loads_correct_template(self):
        """
        Test if view function for home loads correct template
        """
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_view_home_template_shows_no_recipe_found_if_no_recipes(self):  # noqa: E501
        """
        Test if home template shows 'No recipe found' if no recipe exists
        """
        Recipe.objects.all().delete()
        response = self.client.get(reverse('recipes:home'))
        info = '<h2>Nenhuma receita encontrada 😢</h2>'
        html_txt = response.content.decode('utf-8')
        self.assertIn(info, html_txt)

    def test_recipe_home_template_loads_recipes(self):
        """
        Test if home template loads recipes
        """
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        # response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertIn('15 minutos', content)
        self.assertIn('4 porções', content)

    def test_recipe_home_template_doesnt_load_recipes_not_published(self):
        """
        Test if home template doesn't load not published recipes
        """
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn('<h2>Nenhuma receita encontrada 😢</h2>', content)

    def test_recipe_home_template_is_paginated(self):
        for i in range(18):
            kwargs = {
                'author_data': {'username': f'user{i}'},
                'slug': f'recipe-{i}'
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            # Testing total of pages
            num_pages_wanted = 6
            self.assertEqual(
                paginator.num_pages,
                num_pages_wanted,
                msg=f'Home template must have {paginator.num_pages} pages but'
                f' found {num_pages_wanted}'
            )

            # Testing items by page
            num_items_wanted = 3
            self.assertEqual(
                len(paginator.get_page(1)),
                num_items_wanted,
                msg=f'One page in Home template must have '
                f'{paginator.num_pages} but found {num_items_wanted}'
            )

    def test_recipe_home__invalid_page_query_uses_page_one(self):
        for i in range(8):
            kwargs = {
                'author_data': {'username': f'user{i}'},
                'slug': f'recipe-{i}'
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1A')
            self.assertEqual(
                response.context['recipes'].number,
                1,
                msg='If page query is invalid, Home template must load page 1'
            )
        
