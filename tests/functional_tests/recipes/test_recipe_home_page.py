import pytest
from selenium.webdriver.common.by import By

from recipes.tests.test_recipe_base import RecipeMixin

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest, RecipeMixin):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nenhuma receita encontrada 😢', body.text)
