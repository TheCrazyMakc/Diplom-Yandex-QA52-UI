# UI-тесты для Stellar Burgers

Набор UI-тестов (Selenium + Pytest) для https://stellarburgers.education-services.ru/ с паттерном Page Object и
аллюр-шагами.

## Требования

- Python 3.10+
- Google Chrome и Mozilla Firefox
- pip install -r requirements.txt

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

- Все тесты (Chrome и Firefox параметризовано):

```bash
pytest -q
```

- Только файл:

```bash
pytest -q tests/test_order_feed.py
```

- Конкретный тест:

```bash
pytest -q tests/test_order_feed.py::TestOrderFeed::test_total_orders_counter_increases
```

- Запуск только в одном браузере (через отбор по id):

```bash
pytest -q -k "[chrome]"
pytest -q -k "[firefox]"
```

## Allure-отчёт

```bash
pytest -q --alluredir=allure-results
allure serve allure-results
```

## Пользователь для авторизации

Создан заранее через API, хранится в data/user_data.py:

- email: mroizo@mail.ru
- password: password
- name: Quentin Dupieux

## Что проверяется

- Главная:
    - Переход в «Конструктор»
    - Переход в «Ленту заказов»
    - Модалка ингредиента: открытие и закрытие
    - Счётчик ингредиента увеличивается после добавления
- Лента заказов:
    - «Выполнено за всё время» увеличивается после создания заказа
    - «Выполнено за сегодня» увеличивается после создания заказа
    - Номер заказа появляется в разделе «В работе»

## Структура проекта

```
Diplom_3/
├─ conftest.py                 # фикстуры pytest: инициализация драйвера, логин
├─ requirements.txt            # зависимости проекта
├─ README.md                   # описание и инструкция по запуску
├─ data/
│  ├─ urls.py                  # базовые URL приложения
│  └─ user_data.py             # данные тестового пользователя (создан через API)
├─ locators/
│  ├─ main_page_locators.py    # локаторы главной страницы/конструктора
│  ├─ feed_page_locators.py    # локаторы ленты заказов (счётчики, «В работе»)
│  └─ login_page_locators.py   # локаторы страницы логина
├─ pages/
│  ├─ base_page.py             # базовые методы Page Object (ожидания, клики, dnd)
│  ├─ main_page.py             # действия на главной: создание заказа и т.п.
│  ├─ login_page.py            # действия для авторизации
│  └─ feed_page.py             # действия и проверки для ленты заказов
└─ tests/
   ├─ test_main_page.py        # базовые UI-проверки главной
   └─ test_order_feed.py       # проверки счётчиков и «В работе»
```
