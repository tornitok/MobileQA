# Mobile QA Automation Framework

Фреймворк для автоматизированного тестирования мобильных приложений на базе Appium и Python.

## Структура проекта

```
MobileQA/
├── apps/
│   ├── android/            # APK файлы приложения
│   │   └── app.apk
│   └── ios/                # APP/IPA файлы приложения
│       └── app.app
├── config/
│   ├── __init__.py
│   └── config.py           # Конфигурация проекта
├── pages/
│   ├── __init__.py
│   ├── base_page.py        # Базовый класс страниц
│   ├── login_page.py       # Page Object для страницы авторизации
│   └── home_page.py        # Page Object для главной страницы
├── tests/
│   ├── __init__.py
│   ├── test_login.py       # Тесты авторизации
│   └── test_home.py        # Тесты главной страницы
├── utils/
│   ├── __init__.py
│   └── helpers.py          # Вспомогательные функции
├── conftest.py             # Pytest fixtures
├── pytest.ini              # Конфигурация pytest
├── requirements.txt        # Зависимости
├── .env.example            # Пример файла переменных окружения
└── README.md
```

## Установка

### 1. Клонирование и настройка окружения

```bash
cd MobileQA
python -m venv .venv
source .venv/bin/activate  # для macOS/Linux
# или
.venv\Scripts\activate     # для Windows
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Добавление билдов приложения

Поместите билды приложения в соответствующие папки:
- Android: `apps/android/app.apk`
- iOS: `apps/ios/app.app`

Билды хранятся в репозитории и автоматически используются при запуске тестов.

### 4. Настройка переменных окружения (опционально)

```bash
cp .env.example .env
# Отредактируйте .env файл, если нужно переопределить настройки
```

### 5. Установка Appium

```bash
npm install -g appium
appium driver install uiautomator2  # для Android
appium driver install xcuitest      # для iOS
```

## Запуск тестов

### Запуск всех тестов

```bash
pytest
```

### Запуск тестов для Android

```bash
pytest --platform=android
```

### Запуск тестов для iOS

```bash
pytest --platform=ios
```

### Запуск с генерацией Allure отчета

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

### Запуск конкретного теста

```bash
pytest tests/test_login.py::TestLogin::test_successful_login
```

### Запуск по маркерам

```bash
pytest -m smoke
pytest -m regression
```

## Добавление новых тестов

### 1. Создайте Page Object

```python
# pages/new_page.py
from pages.base_page import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class NewPage(BasePage):
    # Локаторы
    ELEMENT = (AppiumBy.ID, "com.example.app:id/element")
    
    def action(self):
        self.click(self.ELEMENT)
        return self
```

### 2. Создайте тест

```python
# tests/test_new_feature.py
import allure
from pages.new_page import NewPage

@allure.feature("Новая фича")
class TestNewFeature:
    
    @allure.title("Тест новой фичи")
    def test_new_feature(self, driver):
        page = NewPage(driver)
        page.action()
        assert page.is_element_visible(page.ELEMENT)
```

## Полезные команды

```bash
# Запуск Appium сервера
appium

# Список подключенных Android устройств
adb devices

# Список iOS симуляторов
xcrun simctl list devices
```

