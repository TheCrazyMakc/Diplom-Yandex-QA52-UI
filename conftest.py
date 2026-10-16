import pytest
import allure
from selenium import webdriver

from api.user_api import UserApi
from data.urls import Urls
from data.user_data import generate_user_data
from pages.login_page import LoginPage
from pages.main_page import MainPage


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
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
def user_api():
    return UserApi()


@pytest.fixture
def registered_user(user_api):
    """
    Создаёт уникального пользователя через API перед тестом
    и удаляет его после.
    """
    data = generate_user_data()

    with allure.step(f"API: регистрация пользователя {data['email']}"):
        resp = user_api.register(**data)
        assert resp.status_code == 200, f"Не удалось зарегистрировать: {resp.text}"

    login_resp = user_api.login(data["email"], data["password"])
    token = login_resp.json().get("accessToken")
    data["access_token"] = token

    yield data

    with allure.step(f"API: удаление пользователя {data['email']}"):
        if token:
            user_api.delete(token)


@pytest.fixture
def logged_in_driver(driver, registered_user):
    """Открывает страницу логина и авторизует свежесозданного пользователя."""
    with allure.step("Авторизация тестового пользователя"):
        driver.get(Urls.LOGIN_URL)
        LoginPage(driver).login(
            registered_user["email"], registered_user["password"]
        )
        MainPage(driver).wait_for_assemble_burger_title()
    return driver