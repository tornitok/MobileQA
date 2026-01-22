import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Корневая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Конфигурация проекта"""

    # Appium Server
    APPIUM_SERVER_URL = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")

    # Пути к билдам (относительно корня проекта)
    APPS_DIR = BASE_DIR / "apps"

    # Android настройки
    ANDROID_DEVICE_NAME = os.getenv("ANDROID_DEVICE_NAME", "emulator-5554")
    ANDROID_APP_PATH = os.getenv("ANDROID_APP_PATH", str(APPS_DIR / "android" / "webview-sample-debug.apk"))
    ANDROID_PLATFORM_VERSION = os.getenv("ANDROID_PLATFORM_VERSION", "13")

    # iOS настройки
    IOS_DEVICE_NAME = os.getenv("IOS_DEVICE_NAME", "iPhone 14")
    IOS_APP_PATH = os.getenv("IOS_APP_PATH", str(APPS_DIR / "ios" / "app.app"))
    IOS_PLATFORM_VERSION = os.getenv("IOS_PLATFORM_VERSION", "16.0")

    # Таймауты
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))

