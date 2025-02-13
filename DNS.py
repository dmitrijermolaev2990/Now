from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_price():
    """Функция для получения цены товара на сайте DNS-Shop с использованием Selenium"""

    # Инициализация WebDriver для Chrome с дополнительными опциями
    options = Options()
    options.add_argument("--headless")  # Запуск в фоновом режиме (если необходимо)
    options.add_argument("--disable-gpu")  # Для Windows, если есть проблемы с графикой
    options.add_argument("--no-sandbox")

    # Дополнительные заголовки для имитации браузера
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    # Инициализация WebDriver для Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL товара (замени на нужный)
    URL = "https://www.dns-shop.ru/product/ecfdda9c795aed20/142-noutbuk-apple-macbook-pro-cernyj/"

    try:
        # Открытие страницы товара
        driver.get(URL)

        # Даем странице немного времени для загрузки динамического контента
        time.sleep(5)  # Пауза в 5 секунд

        # Получаем HTML-страницу для анализа (для отладки)
        page_source = driver.page_source
        print(page_source[:1000])  # Печатаем первые 1000 символов для анализа

        # Явное ожидание элемента с ценой (попробуем XPath)
        try:
            # Ожидаем, пока элемент с ценой не станет видимым
            price_tag = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'product-card-price__current')]"))
            )
            # Получаем цену и удаляем лишние символы
            price = price_tag.text.strip().replace(" ", "").replace("₽", "")

            # Преобразуем цену в число и возвращаем
            return int(price)
        except Exception as e:
            print(f"Ошибка при поиске элемента с ценой: {e}")
            return None

    except Exception as e:
        print(f"Ошибка при получении страницы: {e}")
        return None

    finally:
        # Закрытие браузера
        driver.quit()


def track_price(threshold_price):
    """Функция для отслеживания цены товара"""
    while True:
        price = get_price()
        if price:
            print(f"Текущая цена: {price} ₽")

            # Если цена ниже порогового значения, уведомляем
            if price <= threshold_price:
                print(f"🔥 Цена упала до {price} ₽! Покупай сейчас!")
                break
        else:
            print("Ошибка получения цены!")

        # Ждем 10 минут перед повторной проверкой
        time.sleep(600)


# Запуск отслеживания
track_price(50000)  # Замените 50000 на желаемую цену
