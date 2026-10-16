from pages.base_page import BasePage
from locators.feed_page_locators import FeedPageLocators
from utils.text import normalize_order_number
import allure


class FeedPage(BasePage):

    @allure.step("Ожидание загрузки счётчиков на странице")
    def wait_for_counters_to_load(self, time_to_wait=10):
        def condition(driver):
            for locator in (
                FeedPageLocators.TOTAL_ORDERS_COUNTER,
                FeedPageLocators.TODAY_ORDERS_COUNTER,
            ):
                text = driver.find_element(*locator).text.strip()
                if not text.isdigit():
                    return False
            return True

        self.wait_for_condition(condition, time=time_to_wait)

    @allure.step("Получение значения счётчика 'Выполнено за все время'")
    def get_total_orders_count(self, time=10):
        return self._get_counter_value(FeedPageLocators.TOTAL_ORDERS_COUNTER, time)

    @allure.step("Получение значения счётчика 'Выполнено за сегодня'")
    def get_today_orders_count(self, time=10):
        return self._get_counter_value(FeedPageLocators.TODAY_ORDERS_COUNTER, time)

    def _get_counter_value(self, locator, time=10):
        def condition(driver):
            text = driver.find_element(*locator).text.strip()
            return int(text) if text.isdigit() else False

        return self.wait_for_condition(condition, time=time)

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
        elements = self.driver.find_elements(*FeedPageLocators.IN_PROGRESS_ORDERS)
        return [
            normalize_order_number(e.text)
            for e in elements
            if e.text.strip()
        ]

    @allure.step("Ожидание появления заказа '{order_number}' в разделе 'В работе'")
    def wait_for_order_in_progress(self, order_number, time=30):
        target = normalize_order_number(order_number)

        def condition(driver):
            elems = driver.find_elements(*FeedPageLocators.IN_PROGRESS_ORDERS)
            return any(normalize_order_number(el.text) == target for el in elems)

        self.wait_for_condition(condition, time=time)