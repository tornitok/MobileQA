import os
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from dotenv import load_dotenv
from config.config import Config

# Загружаем переменные окружения
load_dotenv()

# Устанавливаем ANDROID_HOME для Appium сервера
if os.getenv("ANDROID_HOME"):
    os.environ["ANDROID_HOME"] = os.getenv("ANDROID_HOME")


@pytest.fixture(scope="function")
def driver(request):
    """Создание драйвера для тестов"""
    platform = request.config.getoption("--platform", default="android")

    if platform.lower() == "android":
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = Config.ANDROID_DEVICE_NAME
        options.app = Config.ANDROID_APP_PATH
        options.automation_name = "UiAutomator2"
        options.no_reset = False
    else:
        options = XCUITestOptions()
        options.platform_name = "iOS"
        options.device_name = Config.IOS_DEVICE_NAME
        options.app = Config.IOS_APP_PATH
        options.automation_name = "XCUITest"
        options.no_reset = False

    driver = webdriver.Remote(Config.APPIUM_SERVER_URL, options=options)
    driver.implicitly_wait(Config.IMPLICIT_WAIT)

    yield driver

    driver.quit()


def pytest_addoption(parser):
    """Добавление опций командной строки"""
    parser.addoption(
        "--platform",
        action="store",
        default="android",
        help="Платформа для запуска тестов: android или ios"
    )

