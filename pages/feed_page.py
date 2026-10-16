from pages.base_page import BasePage
from locators.feed_page_locators import FeedPageLocators
import allure


class FeedPage(BasePage):
    """
    Класс страницы ленты заказов, содержащий методы для получения информации о заказах.
    """
    @allure.step("Ожидание загрузки счетчиков на странице")
    def wait_for_counters_to_load(self, time_to_wait=10):
        """Ожидает загрузки счетчиков на странице."""
        self.wait_for_element_visibility(FeedPageLocators.TOTAL_ORDERS_COUNTER, time=time_to_wait)

    @allure.step("Получение значения счетчика 'Выполнено за все время'")
    def get_total_orders_count(self):
        """Получает значение счетчика 'Выполнено за все время'."""
        return int(self.find_element(FeedPageLocators.TOTAL_ORDERS_COUNTER).text)

    @allure.step("Получение значения счетчика 'Выполнено за сегодня'")
    def get_today_orders_count(self):
        """Получает значение счетчика 'Выполнено за сегодня'."""
        return int(self.find_element(FeedPageLocators.TODAY_ORDERS_COUNTER).text)

    @allure.step("Ожидание увеличения счетчика 'Выполнено за все время'")
    def wait_for_total_orders_to_increase(self, initial_count, time=10):
        """Ожидает, пока счетчик 'Выполнено за все время' не увеличится."""
        def condition(driver):
            return self.get_total_orders_count() > initial_count

        self.wait_for_condition(condition, time=time)

    @allure.step("Ожидание увеличения счетчика 'Выполнено за сегодня'")
    def wait_for_today_orders_to_increase(self, initial_count, time=10):
        """Ожидает, пока счетчик 'Выполнено за сегодня' не увеличится."""
        def condition(driver):
            return self.get_today_orders_count() > initial_count

        self.wait_for_condition(condition, time=time)

    @allure.step("Получение списка номеров заказов в разделе 'В работе'")
    def get_in_progress_orders(self):
        """Получает список номеров заказов в разделе 'В работе'."""
        elements = self.driver.find_elements(*FeedPageLocators.IN_PROGRESS_ORDERS)
        numbers = []
        for e in elements:
            merged = ''.join(ch for ch in e.text if ch.isdigit()).lstrip('0') or '0'
            if merged:
                numbers.append(merged)
        return numbers

    @allure.step("Ожидание появления заказа '{order_number}' в разделе 'В работе'")
    def wait_for_order_in_progress(self, order_number, time=30):
        """Ожидает появления указанного номера заказа в разделе 'В работе'."""
        order_number = str(order_number).strip()

        def condition(driver):
            elems = driver.find_elements(*FeedPageLocators.IN_PROGRESS_ORDERS)
            for el in elems:
                merged = ''.join(ch for ch in el.text if ch.isdigit()).lstrip('0') or '0'
                if merged == order_number:
                    return True
            return False

        self.wait_for_condition(condition, time=time)
