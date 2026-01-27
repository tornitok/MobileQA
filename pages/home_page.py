from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from pages.webview_page import WebViewPage
from pages.simple_fragment_page import SimpleFragmentPage


class HomePage(BasePage):
    """Главная страница"""

    # Локаторы
    WEBVIEW_BUTTON = (AppiumBy.ID, "com.kaspersky.kaspressample:id/activity_main_webview_sample_button")
    MAIN_SCREEN_TEXT = (AppiumBy.ID, "com.kaspersky.kaspressample:id/activity_main_title")
    SIMPLE_FRAGMENT_BUTTON = (AppiumBy.ID, "com.kaspersky.kaspressample:id/activity_main_simple_sample_button")

    def __init__(self, driver):
        super().__init__(driver)

    def is_home_page_displayed(self):
        """Проверить отображение главной страницы"""
        return self.is_element_visible(self.MAIN_SCREEN_TEXT)

    def open_webview_screen(self):
        """Открыть экран с WebView"""
        self.click(self.WEBVIEW_BUTTON)
        return WebViewPage(self.driver)

    def open_simple_fragment_screen(self):
        """Открыть экран с простым фрагментом"""
        self.click(self.SIMPLE_FRAGMENT_BUTTON)
        return SimpleFragmentPage(self.driver)
