import uiautomator2 as u2
import argparse
import subprocess
import json
import re
from pathlib import Path
import sys


BASE_DIR = Path(__file__).parent.parent


def connect_device():
    """Подключение к устройству"""
    print("Подключаюсь к устройству...")
    d = u2.connect()  # Подключается к первому доступному устройству
    print(f"Подключено: {d.info.get('productName', 'Unknown')} ({d.serial})")
    return d


def get_page_source():
    """Получить XML-дерево элементов текущего экрана"""
    d = connect_device()

    print("\n" + "=" * 60)
    print("PAGE SOURCE (XML иерархия элементов):")
    print("=" * 60 + "\n")

    # Получаем XML-структуру экрана
    xml = d.dump_hierarchy()
    print(xml)

    # Сохраняем в файл
    output_file = BASE_DIR / "page_source.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"\n\nСохранено в: {output_file}")


def find_by_class(class_name):
    """Найти все элементы по классу"""
    d = connect_device()

    # Добавляем полный путь класса если нужно
    if not class_name.startswith("android."):
        class_name = f"android.widget.{class_name}"

    print(f"\nИщу элементы с классом: {class_name}")
    print("=" * 60)

    elements = d(className=class_name)
    count = elements.count

    print(f"Найдено: {count} элементов\n")

    for i in range(count):
        el = elements[i]
        info = el.info
        print(f"[{i + 1}] {class_name}")
        print(f"    text: {info.get('text', '')}")
        print(f"    resource-id: {info.get('resourceId', '')}")
        print(f"    content-desc: {info.get('contentDescription', '')}")
        print(f"    bounds: {info.get('bounds', {})}")
        print(f"    clickable: {info.get('clickable', False)}")
        print()


def find_by_text(text):
    """Найти элементы по тексту"""
    d = connect_device()

    print(f"\nИщу элементы с текстом: '{text}'")
    print("=" * 60)

    # Точное совпадение
    elements = d(text=text)
    if elements.count == 0:
        # Частичное совпадение
        elements = d(textContains=text)

    count = elements.count
    print(f"Найдено: {count} элементов\n")

    for i in range(count):
        el = elements[i]
        info = el.info
        print(f"[{i + 1}] {info.get('className', '')}")
        print(f"    text: {info.get('text', '')}")
        print(f"    resource-id: {info.get('resourceId', '')}")
        print(f"    content-desc: {info.get('contentDescription', '')}")
        print(f"    bounds: {info.get('bounds', {})}")
        print()


def find_by_id(resource_id):
    """Найти элемент по resource-id"""
    d = connect_device()

    print(f"\nИщу элемент с resource-id: '{resource_id}'")
    print("=" * 60)

    elements = d(resourceId=resource_id)
    count = elements.count
    print(f"Найдено: {count} элементов\n")

    for i in range(count):
        el = elements[i]
        info = el.info
        print(f"[{i + 1}] {info.get('className', '')}")
        print(f"    text: {info.get('text', '')}")
        print(f"    resource-id: {info.get('resourceId', '')}")
        print(f"    content-desc: {info.get('contentDescription', '')}")
        print()


def take_screenshot():
    """Сделать скриншот"""
    d = connect_device()

    screenshot_path = BASE_DIR / "screenshot.png"
    d.screenshot(str(screenshot_path))
    print(f"\nСкриншот сохранен: {screenshot_path}")


def device_info():
    """Информация об устройстве"""
    d = connect_device()

    print("\nИнформация об устройстве:")
    print("=" * 60)
    info = d.info
    for key, value in info.items():
        print(f"  {key}: {value}")

    print(f"\n  Serial: {d.serial}")
    print(f"  Window size: {d.window_size()}")


def get_webview_elements():
    """
    Получить элементы из WebView через Chrome DevTools Protocol.
    Требуется: WebView должен быть в режиме отладки (setWebContentsDebuggingEnabled(true))
    """
    d = connect_device()

    print("\n" + "=" * 60)
    print("WEBVIEW ELEMENTS")
    print("=" * 60)

    # Включаем port forwarding для Chrome DevTools
    # Находим WebView процесс
    result = subprocess.run(
        ["adb", "shell", "cat", "/proc/net/unix"],
        capture_output=True, text=True
    )

    # Ищем webview socket
    webview_sockets = []
    for line in result.stdout.split('\n'):
        if 'webview_devtools_remote' in line or 'chrome_devtools_remote' in line:
            # Извлекаем имя сокета
            match = re.search(r'@([a-zA-Z_0-9]+_devtools_remote_?\d*)', line)
            if match:
                webview_sockets.append(match.group(1))

    if not webview_sockets:
        print("\nWebView не найден или отладка не включена!")
        print("\nУбедитесь что:")
        print("1. Приложение открыто на экране с WebView")
        print("2. WebView имеет включенную отладку:")
        print("   WebView.setWebContentsDebuggingEnabled(true)")
        return

    print(f"\nНайдены WebView сокеты: {webview_sockets}")

    socket_name = webview_sockets[0]
    local_port = 9222

    # Устанавливаем port forwarding
    subprocess.run(
        ["adb", "forward", f"tcp:{local_port}", f"localabstract:{socket_name}"],
        capture_output=True
    )

    print(f"Port forwarding: localhost:{local_port} -> {socket_name}")

    try:
        import requests

        # Получаем список страниц
        response = requests.get(f"http://localhost:{local_port}/json")
        pages = response.json()

        if not pages:
            print("Нет открытых страниц в WebView")
            return

        print(f"\nНайдено страниц: {len(pages)}")
        for i, page in enumerate(pages):
            print(f"\n[{i + 1}] {page.get('title', 'No title')}")
            print(f"    URL: {page.get('url', '')}")
            print(f"    Type: {page.get('type', '')}")

        # Берем первую страницу
        page = pages[0]
        ws_url = page.get('webSocketDebuggerUrl')

        if ws_url:
            print(f"\nWebSocket URL: {ws_url}")
            print("\nДля просмотра в Chrome DevTools откройте:")
            print(f"  chrome://inspect/#devices")
            print(f"\nИли напрямую: {page.get('devtoolsFrontendUrl', '')}")

        # Получаем DOM через HTTP endpoint
        page_id = page.get('id')

        # Пробуем получить HTML
        print("\n" + "=" * 60)
        print("Для получения HTML откройте Chrome и перейдите:")
        print("  chrome://inspect/#devices")
        print("Затем нажмите 'inspect' под вашим WebView")
        print("=" * 60)

    except ImportError:
        print("\nУстановите requests: pip install requests")
    except Exception as e:
        print(f"\nОшибка: {e}")
    finally:
        # Убираем port forwarding
        subprocess.run(["adb", "forward", "--remove", f"tcp:{local_port}"], capture_output=True)


def click_and_get_webview(resource_id):
    """
    Кликнуть по элементу и получить элементы WebView.
    Пример: python utils/get_page_source.py --click-webview "com.kaspersky.kaspressample:id/activity_main_webview_sample_button"
    """
    d = connect_device()

    print(f"\nКликаю по элементу: {resource_id}")

    # Кликаем по кнопке
    element = d(resourceId=resource_id)
    if element.exists:
        element.click()
        print("Клик выполнен, ожидаю загрузку WebView...")
        import time
        time.sleep(3)  # Ждем загрузку WebView

        # Получаем page source после перехода
        print("\n" + "=" * 60)
        print("PAGE SOURCE после перехода в WebView:")
        print("=" * 60)

        xml = d.dump_hierarchy()

        # Сохраняем
        output_file = BASE_DIR / "webview_page_source.xml"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"\nСохранено в: {output_file}")

        # Ищем WebView элементы
        webviews = d(className="android.webkit.WebView")
        if webviews.exists:
            print(f"\nНайден WebView!")
            print(f"  bounds: {webviews.info.get('bounds')}")

            # Пробуем получить элементы через Chrome DevTools
            get_webview_elements()
        else:
            print("\nWebView не найден на экране")
            print(xml)
    else:
        print(f"Элемент с id '{resource_id}' не найден!")


def interactive_mode():
    """Интерактивный режим для исследования UI"""
    d = connect_device()

    print("\nИнтерактивный режим. Команды:")
    print("  xml      - показать XML иерархию")
    print("  shot     - сделать скриншот")
    print("  info     - информация об устройстве")
    print("  t:текст  - найти по тексту")
    print("  c:класс  - найти по классу")
    print("  i:id     - найти по resource-id")
    print("  q        - выход")
    print("=" * 60)

    while True:
        try:
            cmd = input("\n> ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if cmd == "q":
            break
        elif cmd == "xml":
            print(d.dump_hierarchy())
        elif cmd == "shot":
            d.screenshot(str(BASE_DIR / "screenshot.png"))
            print("Скриншот сохранен")
        elif cmd == "info":
            print(d.info)
        elif cmd.startswith("t:"):
            text = cmd[2:]
            els = d(textContains=text)
            for i in range(els.count):
                print(els[i].info)
        elif cmd.startswith("c:"):
            cls = cmd[2:]
            if not cls.startswith("android."):
                cls = f"android.widget.{cls}"
            els = d(className=cls)
            for i in range(els.count):
                print(els[i].info)
        elif cmd.startswith("i:"):
            rid = cmd[2:]
            els = d(resourceId=rid)
            for i in range(els.count):
                print(els[i].info)
        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Получение локаторов элементов через uiautomator2")
    parser.add_argument("--class", dest="class_name", help="Найти по классу (Button, EditText, TextView...)")
    parser.add_argument("--text", dest="text", help="Найти по тексту")
    parser.add_argument("--id", dest="resource_id", help="Найти по resource-id")
    parser.add_argument("--screenshot", action="store_true", help="Сделать скриншот")
    parser.add_argument("--info", action="store_true", help="Информация об устройстве")
    parser.add_argument("-i", "--interactive", action="store_true", help="Интерактивный режим")
    parser.add_argument("--webview", action="store_true", help="Получить элементы из WebView")
    parser.add_argument("--click-webview", dest="click_webview", help="Кликнуть по элементу и получить WebView (resource-id)")

    args = parser.parse_args()

    if args.class_name:
        find_by_class(args.class_name)
    elif args.text:
        find_by_text(args.text)
    elif args.resource_id:
        find_by_id(args.resource_id)
    elif args.screenshot:
        take_screenshot()
    elif args.info:
        device_info()
    elif args.interactive:
        interactive_mode()
    elif args.webview:
        get_webview_elements()
    elif args.click_webview:
        click_and_get_webview(args.click_webview)
    else:
        get_page_source()
