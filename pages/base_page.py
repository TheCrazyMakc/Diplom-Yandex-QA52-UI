from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class BasePage:
    """
    Базовый класс для всех Page Object.
    Содержит общие методы для взаимодействия с веб-страницами.
    """

    def __init__(self, driver):
        """
        Инициализирует базовую страницу.
        :param driver: Экземпляр веб-драйвера.
        """
        self.driver = driver

    @allure.step("Найти элемент по локатору {locator}")
    def find_element(self, locator, time=10):
        """
        Находит один веб-элемент по локатору с ожиданием.
        :param locator: Кортеж (By, 'selector').
        :param time: Время ожидания в секундах.
        :return: Найденный веб-элемент.
        """
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Can't find element by locator {locator}"
        )

    @allure.step("Найти элементы по локатору {locator}")
    def find_elements(self, locator, time=10):
        """
        Находит все веб-элементы по локатору с ожиданием.
        :param locator: Кортеж (By, 'selector').
        :param time: Время ожидания в секундах.
        :return: Список найденных веб-элементов.
        """
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Can't find elements by locator {locator}"
        )

    @allure.step("Кликнуть на элемент по локатору {locator}")
    def click_on_element(self, locator):
        """
        Кликает на веб-элемент.
        :param locator: Кортеж (By, 'selector').
        """
        self.find_element(locator).click()

    @allure.step("Ожидать кликабельности элемента по локатору {locator}")
    def wait_for_element_to_be_clickable(self, locator, time=5):
        """
        Ожидает, пока элемент не станет кликабельным.
        :param locator: Кортеж (By, 'selector').
        :param time: Время ожидания в секундах.
        """
        return WebDriverWait(self.driver, time).until(
            EC.element_to_be_clickable(locator)
        )

    @allure.step("Ожидать видимости элемента по локатору {locator}")
    def wait_for_element_visibility(self, locator, time=5):
        """
        Ожидает, пока элемент не станет видимым.
        :param locator: Кортеж (By, 'selector').
        :param time: Время ожидания в секундах.
        """
        return WebDriverWait(self.driver, time).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step("Ожидать невидимости элемента по локатору {locator}")
    def wait_for_element_invisibility(self, locator, time=5):
        """
        Ожидает, пока элемент не станет невидимым.
        :param locator: Кортеж (By, 'selector').
        :param time: Время ожидания в секундах.
        """
        return WebDriverWait(self.driver, time).until(
            EC.invisibility_of_element_located(locator)
        )

    @allure.step("Ожидать URL: {url}")
    def wait_for_url_to_be(self, url, time=5):
        """
        Ожидает, пока URL страницы не станет равным указанному.
        :param url: Ожидаемый URL.
        :param time: Время ожидания в секундах.
        """
        WebDriverWait(self.driver, time).until(EC.url_to_be(url))

    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Возвращает текущий URL страницы."""
        return self.driver.current_url

    @allure.step("Проверить, открыт ли URL ленты заказов")
    def is_feed_url(self):
        """
        Проверяет, открыт ли URL ленты заказов.
        :return: True, если URL ленты заказов открыт, иначе False.
        """
        current = self.get_current_url()
        return current.endswith("/feed") or "/feed" in current

    @allure.step("Ожидать выполнения условия")
    def wait_for_condition(self, condition, time=5):
        """
        Ожидает выполнения произвольного условия.
        :param condition: Функция условия, которая должна вернуть True.
        :param time: Время ожидания в секундах.
        """
        return WebDriverWait(self.driver, time).until(condition)

    @allure.step("Кликнуть на элемент по локатору {locator} с помощью JS")
    def js_click(self, locator):
        """
        Выполняет клик с помощью JavaScript, чтобы обойти перекрытие элементов.
        :param locator: Кортеж (By, 'selector').
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Перетащить элемент из {source_locator} в {target_locator} с помощью JS")
    def drag_and_drop(self, source_locator, target_locator):
        """
        Выполняет перетаскивание элемента с помощью JavaScript.
        :param source_locator: Локатор исходного элемента.
        :param target_locator: Локатор целевого элемента.
        """
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)

        self.driver.execute_script("""
            function createEvent(type) {
                var event = document.createEvent('CustomEvent');
                event.initCustomEvent(type, true, true, null);
                event.dataTransfer = {
                    data: {},
                    setData: function(type, val) {
                        this.data[type] = val;
                    },
                    getData: function(type) {
                        return this.data[type];
                    }
                };
                return event;
            }

            function dispatchEvent(element, event, transferData) {
                if (transferData !== undefined) {
                    event.dataTransfer = transferData;
                }
                if (element.dispatchEvent) {
                    element.dispatchEvent(event);
                } else if (element.fireEvent) {
                    element.fireEvent('on' + event.type, event);
                }
            }

            var source = arguments[0];
            var target = arguments[1];

            var dragStartEvent = createEvent('dragstart');
            dispatchEvent(source, dragStartEvent);

            var dragEnterEvent = createEvent('dragenter');
            dispatchEvent(target, dragEnterEvent);

            var dragOverEvent = createEvent('dragover');
            dispatchEvent(target, dragOverEvent);

            var dropEvent = createEvent('drop');
            dispatchEvent(target, dropEvent, dragStartEvent.dataTransfer);

            var dragEndEvent = createEvent('dragend');
            dispatchEvent(source, dragEndEvent, dragStartEvent.dataTransfer);
        """, source, target)
