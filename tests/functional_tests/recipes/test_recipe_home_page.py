from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from recipes.tests.test_recipe_base import RecipeMixin

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest, RecipeMixin):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita encontrada 😢', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipes_in_batch()

        # User opens the home page
        self.browser.get(self.live_server_url)
        self.sleep()

        # He sees a text field with 'Type something here to search'
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Type something here to search"]'
        )

        # Clicks in field and types the search text "Recipe Title N.º 1"
        # to find a recipe
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        container = self.browser.find_element(
            By.CLASS_NAME, 'main-content-list').text

        self.sleep(6)

        self.assertIn(
            recipes[0].title,
            container
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipes_in_batch()

        # User opens the home page
        self.browser.get(self.live_server_url)

        self.sleep(6)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_home_page_pagination(self):
        # Creating 10 recipes
        self.make_recipes_in_batch(qtd=20)

        # User opens the home page
        self.browser.get(self.live_server_url)
        self.sleep(1)

        # User sees pagination and click on page 2 link
        page_2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )

        page_2.click()

        # User sees 2 more recipes in page
        total_recipes_in_page = len(self.browser.find_elements(
            By.CLASS_NAME, 'recipe-list-item'))

        self.assertEqual(
            2,
            total_recipes_in_page
        )
