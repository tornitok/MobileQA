import pytest
from pages.home_page import HomePage


class TestFlaky:
    """Тесты Flaky Sample"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Предусловие: открыть приложение"""
        self.home_page = HomePage(driver)

    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_flaky_sample(self):
        assert self.home_page.is_home_page_displayed(), "Главная страница не отображается"
        self.home_page.take_screenshot("home_page")

        flaky_page = self.home_page.open_flaky_screen()
        flaky_page.take_screenshot("flaky_screen")
        assert flaky_page.is_flaky_page_displayed(), "Flaky страница не отображается"

        total_buttons = flaky_page.get_total_buttons_count()
        flaky_page.take_screenshot("buttons_count")
        assert total_buttons == 4, f"Ожидалось 4 кнопки, найдено {total_buttons}"

        flaky_page.scroll_to_button_5()
        flaky_page.take_screenshot("after_scroll")

        flaky_page.click_button_5()
        flaky_page.take_screenshot("after_click_button")

        last_text = flaky_page.get_text_view_6_text()
        flaky_page.take_screenshot("last_text_view")
        assert last_text == "TextView", f"Ожидался текст 'TextView', получен '{last_text}'"
