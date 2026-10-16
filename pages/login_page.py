from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators
import allure


class LoginPage(BasePage):
    """
    Класс страницы входа, содержащий методы для авторизации пользователя.
    """
    @allure.step("Ввод email")
    def set_email(self, email):
        """Вводит email в соответствующее поле."""
        self.wait_for_element_visibility(LoginPageLocators.EMAIL_INPUT)
        self.find_element(LoginPageLocators.EMAIL_INPUT).send_keys(email)

    @allure.step("Ввод пароля")
    def set_password(self, password):
        """Вводит пароль в соответствующее поле."""
        self.wait_for_element_visibility(LoginPageLocators.PASSWORD_INPUT)
        self.find_element(LoginPageLocators.PASSWORD_INPUT).send_keys(password)

    @allure.step("Нажать кнопку Войти")
    def click_login_button(self):
        """Кликает на кнопку 'Войти'."""
        self.wait_for_element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON)
        self.js_click(LoginPageLocators.LOGIN_BUTTON)

    @allure.step("Авторизация пользователя")
    def login(self, email, password):
        """Выполняет полный процесс входа в систему."""
        self.set_email(email)
        self.set_password(password)
        self.click_login_button()
