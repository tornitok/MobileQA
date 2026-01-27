import pytest
from pages.home_page import HomePage


class TestSimpleFragment:
    """Тесты главной страницы"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Предусловие: авторизоваться в приложении"""
        self.home_page = HomePage(driver)

    def test_input(self):
        """Тест: Получить текст из вебвью"""
        assert self.home_page.is_home_page_displayed(), "Главная страница не отображается"
        simple_fragment_page = self.home_page.open_simple_fragment_screen()
        assert simple_fragment_page.is_simple_button_displayed(), "Кнопка 1 не отображается"
        simple_fragment_page.click_button_1()
        assert simple_fragment_page.is_button_2_displayed(), "Кнопка 2 не отображается"
        simple_fragment_page.click_button_2()
        simple_fragment_page.enter_text()
        simple_fragment_page.text_is_displayed()


