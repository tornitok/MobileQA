from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class HomePage(BasePage):
    """Главная страница"""

    # Локаторы
    WEBVIEW_BUTTON = (AppiumBy.ID, "com.kaspersky.kaspressample:id/activity_main_webview_sample_button")
    MAIN_SCREEN_TEXT = (AppiumBy.ID, "com.kaspersky.kaspressample:id/activity_main_title")

    def __init__(self, driver):
        super().__init__(driver)

    def is_home_page_displayed(self):
        """Проверить отображение главной страницы"""
        return self.is_element_visible(self.MAIN_SCREEN_TEXT)

    def open_webview_screen(self):
        """Открыть экран с WebView"""
        self.click(self.WEBVIEW_BUTTON)
        from pages.webview_page import WebViewPage
        return WebViewPage(self.driver)
