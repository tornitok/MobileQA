import pytest
from pages.home_page import HomePage


class TestHomePage:
    """Тесты главной страницы"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Предусловие: авторизоваться в приложении"""
        self.home_page = HomePage(driver)

    def test_get_text_webview(self):
        """Тест: Получить текст из вебвью"""
        assert self.home_page.is_home_page_displayed(), "Главная страница не отображается"
        webview_page = self.home_page.open_webview_screen()
        webview_text = webview_page.get_webview_text()
        assert webview_text == "Kaspresso is a great framework for UI testing. Based on ", f'{webview_text} текст не совпадает'


