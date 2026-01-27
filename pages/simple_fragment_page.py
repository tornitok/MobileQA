from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from pages.webview_page import WebViewPage


class SimpleFragmentPage(BasePage):
    """Главная страница"""

    # Локаторы
    BUTTON_1 = (AppiumBy.ID, "com.kaspersky.kaspressample:id/button_1")
    BUTTON_2 = (AppiumBy.ID, "com.kaspersky.kaspressample:id/button_2")
    EDIT_FIELD = (AppiumBy.ID, "com.kaspersky.kaspressample:id/edit")

    def __init__(self, driver):
        super().__init__(driver)

    def is_simple_button_displayed(self):
        """Проверить отображение главной страницы"""
        return self.is_element_visible(self.BUTTON_1)

    def click_button_1(self):
        """Открыть экран с WebView"""
        self.click(self.BUTTON_1)

    def is_button_2_displayed(self):
        """Проверить отображение главной страницы"""
        return self.is_element_visible(self.BUTTON_2)

    def click_button_2(self):
        """Открыть экран с WebView"""
        self.click(self.BUTTON_2)

    def enter_text(self):
        """Открыть экран с простым фрагментом"""
        self.send_keys(self.EDIT_FIELD, "Hello World!")

    def text_is_displayed(self, expected_text="Hello World!"):
        """Проверить что текст в поле соответствует ожидаемому"""
        element = self.find_element(self.EDIT_FIELD)
        actual_text = element.get_attribute("text")
        assert actual_text == expected_text, f"Ожидался текст '{expected_text}', но получен '{actual_text}'"
