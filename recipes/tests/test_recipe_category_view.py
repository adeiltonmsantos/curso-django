from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

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

    def test_recipe_view_category_loads_recipes_of_same_category(self):
        """
        Test if category template loads recipes of a category and if
        title is shown correctly
        """
        recipe = self.make_recipe(category_data={'name': 'Category Test'})
        categ_id = recipe.category.id
        categ_name = recipe.category.name

        # Creating another recipe to fail the test ######## # noqa: E266
        # self.make_recipes_with_category_id(categ_id)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': categ_id}))
        qt_recipes = len(response.context['recipes'])
        title_expected = f'{categ_name} - Category | '
        self.assertEqual(
            qt_recipes,
            1,
            msg=f'It should load only {1} recipe(s) but loaded {qt_recipes}'
        )
        self.assertIn(
            title_expected,
            response.context['title'],
            msg=f'The title template should be "{title_expected}" but '
            f'found "{response.context["title"]}"'
        )

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
