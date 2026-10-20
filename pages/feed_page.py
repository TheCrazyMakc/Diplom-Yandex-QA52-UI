from pages.base_page import BasePage
from locators.feed_page_locators import FeedPageLocators
from utils.text import normalize_order_number
import allure


class FeedPage(BasePage):

    @allure.step("Ожидание загрузки счётчиков на странице")
    def wait_for_counters_to_load(self, time_to_wait=10):
        def condition():
            for locator in (
                FeedPageLocators.TOTAL_ORDERS_COUNTER,
                FeedPageLocators.TODAY_ORDERS_COUNTER,
            ):
                text = self.get_element_text_safe(locator)
                if not text or not text.isdigit():
                    return False
            return True

        self.wait_for_condition_no_driver(condition, time=time_to_wait)

    @allure.step("Получение значения счётчика 'Выполнено за все время'")
    def get_total_orders_count(self, time=10):
        return self._get_counter_value(FeedPageLocators.TOTAL_ORDERS_COUNTER, time)

    @allure.step("Получение значения счётчика 'Выполнено за сегодня'")
    def get_today_orders_count(self, time=10):
        return self._get_counter_value(FeedPageLocators.TODAY_ORDERS_COUNTER, time)

    def _get_counter_value(self, locator, time=10):
        result = {}

        def condition():
            text = self.get_element_text_safe(locator)
            if text and text.isdigit():
                result["value"] = int(text)
                return True
            return False

        self.wait_for_condition_no_driver(condition, time=time)
        return result["value"]

    @allure.step("Ожидание увеличения счетчика 'Выполнено за все время'")
    def wait_for_total_orders_to_increase(self, initial_count, time=10):
        self.wait_for_condition_no_driver(
            lambda: self.get_total_orders_count() > initial_count, time=time
        )

    @allure.step("Ожидание увеличения счетчика 'Выполнено за сегодня'")
    def wait_for_today_orders_to_increase(self, initial_count, time=10):
        self.wait_for_condition_no_driver(
            lambda: self.get_today_orders_count() > initial_count, time=time
        )

    @allure.step("Получение списка номеров заказов в разделе 'В работе'")
    def get_in_progress_orders(self):
        elements = self.find_elements_safe(FeedPageLocators.IN_PROGRESS_ORDERS)
        return [
            normalize_order_number(e.text)
            for e in elements
            if e.text.strip()
        ]

    @allure.step("Ожидание появления заказа '{order_number}' в разделе 'В работе'")
    def wait_for_order_in_progress(self, order_number, time=30):
        target = normalize_order_number(order_number)

        def condition():
            elems = self.find_elements_safe(FeedPageLocators.IN_PROGRESS_ORDERS)
            return any(normalize_order_number(el.text) == target for el in elems)

        self.wait_for_condition_no_driver(condition, time=time)