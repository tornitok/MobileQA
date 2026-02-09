import pytest
from faker import Faker
from pages.home_page import HomePage

fake = Faker()


class TestSimpleFragment:
    """Тесты главной страницы"""

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Предусловие: авторизоваться в приложении"""
        self.home_page = HomePage(driver)

    def test_input_with_faker(self):
        """Тест 1: Ввод текста с помощью faker"""
        faker_text = fake.name()

        assert self.home_page.is_home_page_displayed(), "Главная страница не отображается"
        self.home_page.take_screenshot("home_page")

        simple_fragment_page = self.home_page.open_simple_fragment_screen()
        simple_fragment_page.take_screenshot("simple_fragment_screen")

        assert simple_fragment_page.is_simple_button_displayed(), "Кнопка 1 не отображается"
        simple_fragment_page.click_button_1()
        simple_fragment_page.take_screenshot("after_click_button_1")

        assert simple_fragment_page.is_button_2_displayed(), "Кнопка 2 не отображается"
        simple_fragment_page.click_button_2()
        simple_fragment_page.take_screenshot("after_click_button_2")

        simple_fragment_page.enter_text(faker_text)
        simple_fragment_page.take_screenshot("after_enter_text")

        simple_fragment_page.text_is_displayed(faker_text)
        simple_fragment_page.take_screenshot("text_displayed")

    def test_input_with_parameter(self):
        """Тест 2: Ввод текста с помощью параметра"""
        input_text = "Hello World!"

        assert self.home_page.is_home_page_displayed(), "Главная страница не отображается"
        self.home_page.take_screenshot("home_page")

        simple_fragment_page = self.home_page.open_simple_fragment_screen()
        simple_fragment_page.take_screenshot("simple_fragment_screen")

        assert simple_fragment_page.is_simple_button_displayed(), "Кнопка 1 не отображается"
        simple_fragment_page.click_button_1()
        simple_fragment_page.take_screenshot("after_click_button_1")

        assert simple_fragment_page.is_button_2_displayed(), "Кнопка 2 не отображается"
        simple_fragment_page.click_button_2()
        simple_fragment_page.take_screenshot("after_click_button_2")

        simple_fragment_page.enter_text(input_text)
        simple_fragment_page.take_screenshot("after_enter_text")

        simple_fragment_page.text_is_displayed("Hello World!")
        simple_fragment_page.take_screenshot("text_displayed")


