from django.test import TestCase  # import: ignore

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def create_author(
            self,
            first_name='User',
            last_name='Last Name',
            username='username',
            password='123456',
            email='user@email.com'
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def make_recipe(
            self,
            category_data=None,
            author_data=None,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=15,
            preparation_time_unit='minutos',
            servings=4,
            servings_unit='porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=True
    ):
        """
        Creates a recipe for testing, allowing to provide the name of a
        new category. If no name is provided, creates a category with the
        default name 'Category'.
        """
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.create_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )

    def make_recipes_with_category_id(
        self,
        category_id,
        title='Recipe Title',
        description='Recipe Description',
        slug='recipe-slug-for',
        preparation_time=15,
        preparation_time_unit='minutos',
        servings=4,
        servings_unit='porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True
    ):
        """
        Creates a recipe for testing, associating it with an exisiting
        category by its id
        """
        categ = Category.objects.get(id=category_id)

        # Verifying if some user exists
        if not User.objects.exists():
            author = self.create_author()
        else:
            author = User.objects.first()

        return Recipe.objects.create(
            category=categ,
            author=author,
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
