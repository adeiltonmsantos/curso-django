from django.urls import resolve, reverse

from recipes import views
from recipes.models import Recipe

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    # =======================================================
    # ================= Home View Tests =====================
    # =======================================================
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

    # ========= End of Home View Tests =============================

    # =======================================================
    # ================= Recipe View Tests ===================
    # =======================================================

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

    # ========= End of Recipe View Tests ====================

    # =======================================================
    # ================ Category View Tests ==================
    # =======================================================

    def test_recipe_view_category_is_correct(self):
        """
        Test if view function for category is correct
        """
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_view_category_returns_404_if_no_recipes_found(self):
        """
        Test if category template returns 404 if a non existing category
        is requested
        """
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        """
        Test if category template loads a especific recipe
        """
        neeed_title = 'This is a category test'
        self.make_recipe(title=neeed_title)
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        self.assertIn(neeed_title, content)

    def test_recipe_view_category_doesnt_loads_not_published_recipes(self):
        """
        Test if category template doens't load not published recipes
        """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': recipe.category.id})
        )
        self.assertEqual(response.status_code, 404)

    # ========= End of Category View Tests ==================
