import pytest
from selenium import webdriver
from data.urls import Urls
from data.user_data import generate_user_data
from pages.login_page import LoginPage
from pages.main_page import MainPage
import allure


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """
    Фикстура для инициализации и закрытия драйвера.
    Параметризована для запуска тестов в Chrome и Firefox.
    """
    if request.param == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
    elif request.param == "firefox":
        options = webdriver.FirefoxOptions()
        options.set_preference("dom.webnotifications.enabled", False)
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 1080)
    else:
        raise ValueError(f"Browser {request.param} is not supported")

    driver.get(Urls.BASE_URL)

    yield driver

    driver.quit()


@pytest.fixture
def user():
    """
    Фикстура, предоставляющая данные тестового пользователя.
    """
    return generate_user_data()


@pytest.fixture
def logged_in_driver(driver, user):
    """
    Фикстура для выполнения входа в систему.
    Использует существующего пользователя и возвращает драйвер после логина.
    """
    with allure.step("Авторизация тестового пользователя"):
        driver.get(Urls.LOGIN_URL)
        login_page = LoginPage(driver)
        login_page.login(user["email"], user["password"])

        main_page = MainPage(driver)
        main_page.wait_for_assemble_burger_title()

    return driver
