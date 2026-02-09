from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class FlakyPage(BasePage):
    """Страница Flaky Sample"""

    # Локаторы
    SCROLL_VIEW = (AppiumBy.ID, "com.kaspersky.kaspressample:id/scroll_view")
    BUTTON_1 = (AppiumBy.ID, "com.kaspersky.kaspressample:id/scroll_view_btn1")
    BUTTON_2 = (AppiumBy.ID, "com.kaspersky.kaspressample:id/scroll_view_btn2")
    BUTTON_3 = (AppiumBy.ID, "com.kaspersky.kaspressample:id/scroll_view_btn3")
    BUTTON_4 = (AppiumBy.ID, "com.kaspersky.kaspressample:id/scroll_view_btn4")
    TITLE = (AppiumBy.XPATH, "//android.widget.TextView[@text='Flaky sample']")
    ALL_BUTTONS = (AppiumBy.CLASS_NAME, "android.widget.Button")
    SCROLL_VIEW_TEXT_VIEWS = (AppiumBy.CLASS_NAME, "android.widget.TextView")
    # Кнопка 5 и TextView 6 (после прокрутки)
    BUTTON_5 = (AppiumBy.ID, "com.kaspersky.kaspressample:id/scroll_view_btn5")
    TEXT_VIEW_6 = (AppiumBy.ID, "com.kaspersky.kaspressample:id/scroll_view_tv6")
    TEXT_VIEW_6_XPATH = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='com.kaspersky.kaspressample:id/scroll_view_tv6']")

    def __init__(self, driver):
        super().__init__(driver)

    def is_flaky_page_displayed(self) -> bool:
        """Проверить отображение Flaky страницы"""
        return self.is_element_visible(self.TITLE)

    def get_buttons_count(self) -> int:
        """Подсчитать количество видимых кнопок на экране"""
        buttons = self.find_elements(self.ALL_BUTTONS)
        return len(buttons)

    def get_total_buttons_count(self) -> int:
        """Подсчитать общее количество кнопок (с прокруткой)"""
        total_buttons = set()

        buttons = self.find_elements(self.ALL_BUTTONS)
        for btn in buttons:
            total_buttons.add(btn.get_attribute("resource-id"))

        self.scroll_down()
        buttons = self.find_elements(self.ALL_BUTTONS)
        for btn in buttons:
            total_buttons.add(btn.get_attribute("resource-id"))

        return len(total_buttons)

    def scroll_to_button(self):
        """Проскроллить до кнопки"""
        self.scroll_down()

    def scroll_to_button_5(self):
        """Проскроллить до кнопки 5 и TextView 6"""
        for _ in range(5):
            self.scroll_down()
            if self.is_element_present(self.TEXT_VIEW_6, timeout=2):
                break

    def click_button_1(self):
        """Нажать на кнопку 1"""
        self.click(self.BUTTON_1)

    def click_button_2(self):
        """Нажать на кнопку 2"""
        self.click(self.BUTTON_2)

    def click_button_3(self):
        """Нажать на кнопку 3"""
        self.click(self.BUTTON_3)

    def click_button_4(self):
        """Нажать на кнопку 4"""
        self.click(self.BUTTON_4)

    def get_last_text_view_text(self) -> str:
        """Получить текст последнего TextView внутри ScrollView"""
        text_views = self.find_elements(self.SCROLL_VIEW_TEXT_VIEWS)
        if text_views:
            return text_views[-1].text
        return ""

    def click_button_5(self):
        """Нажать на кнопку 5"""
        self.click(self.BUTTON_5)

    def get_text_view_6_text(self) -> str:
        """Получить текст TextView 6"""
        return self.get_text(self.TEXT_VIEW_6)

