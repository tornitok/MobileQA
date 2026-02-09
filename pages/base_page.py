import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def take_screenshot(self, name: str):
        """Снять скриншот и прикрепить к Allure отчету"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    def find_element(self, locator):
        """Найти элемент"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        """Найти несколько элементов"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """Кликнуть по элементу"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator, text):
        """Ввести текст в элемент"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Получить текст элемента"""
        element = self.find_element(locator)
        return element.text

    def is_element_visible(self, locator, timeout=None):
        """Проверить видимость элемента"""
        try:
            wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def is_element_present(self, locator, timeout=None):
        """Проверить наличие элемента"""
        try:
            wait = WebDriverWait(self.driver, timeout or Config.EXPLICIT_WAIT)
            wait.until(EC.presence_of_element_located(locator))
            return True
        except:
            return False

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 1000):
        """Свайп по координатам"""
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def scroll_down(self):
        """Прокрутка вниз"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.8)
        end_y = int(size['height'] * 0.2)
        self.swipe(start_x, start_y, start_x, end_y)

    def scroll_up(self):
        """Прокрутка вверх"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = int(size['height'] * 0.2)
        end_y = int(size['height'] * 0.8)
        self.swipe(start_x, start_y, start_x, end_y)

    def hide_keyboard(self):
        """Скрыть клавиатуру"""
        try:
            self.driver.hide_keyboard()
        except:
            pass
