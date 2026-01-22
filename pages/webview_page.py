from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class WebViewPage(BasePage):
    """Страница с WebView"""

    # Локаторы
    WEBVIEW_CONTAINER = (AppiumBy.CLASS_NAME, "android.webkit.WebView")
    WEBVIEW_TEXT = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Kaspresso is a great framework for UI testing')]")

    def __init__(self, driver):
        super().__init__(driver)

    def is_webview_displayed(self):
        """Проверить отображение WebView"""
        return self.is_element_visible(self.WEBVIEW_CONTAINER)

    def get_webview_text(self):
        """Получить текст из WebView"""
        return self.get_text(self.WEBVIEW_TEXT)

    def get_all_webview_texts(self):
        """Получить все тексты из WebView"""
        elements = self.find_elements(self.WEBVIEW_TEXT)
        return [el.text for el in elements if el.text]

