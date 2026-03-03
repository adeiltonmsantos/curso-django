from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By

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
        # User opens the home page
        self.browser.get(self.live_server_url)

        # He sees a text field with 'Type something here to search'
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Type something here to search"]'
        )

        # Clicks in field e types the search text "Recipe Title N.º 1" to find
        # a recipe
        search_input.send_keys('Recipe Title N.º 1')

        self.sleep(6)
