from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

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

    def scroll_down(self):
        """Прокрутка вниз"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 0.8
        end_y = size['height'] * 0.2
        self.driver.swipe(start_x, start_y, start_x, end_y, 1000)

    def scroll_up(self):
        """Прокрутка вверх"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 0.2
        end_y = size['height'] * 0.8
        self.driver.swipe(start_x, start_y, start_x, end_y, 1000)

    def hide_keyboard(self):
        """Скрыть клавиатуру"""
        try:
            self.driver.hide_keyboard()
        except:
            pass

    def take_screenshot(self, name):
        """Сделать скриншот"""
        self.driver.save_screenshot(f"screenshots/{name}.png")

