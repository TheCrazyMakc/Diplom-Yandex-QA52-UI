from pages.main_page import MainPage
from pages.feed_page import FeedPage
from data.urls import Urls
import allure


@allure.suite("Лента заказов")
class TestOrderFeed:
    """
    Тесты для проверки функциональности ленты заказов.
    """

    @allure.title("При создании заказа счетчик 'Выполнено за все время' увеличивается")
    def test_total_orders_counter_increases(self, logged_in_driver):
        """
        Проверяет, что после создания нового заказа счетчик "Выполнено за всё время" увеличивается.
        """
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        with allure.step("Шаг 1: Получить начальное значение счетчика 'Выполнено за всё время'"):
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)
            feed_page.wait_for_counters_to_load()
            initial_total_orders = feed_page.get_total_orders_count()

        with allure.step("Шаг 2: Создать новый заказ"):
            main_page.click_constructor_button()
            main_page.wait_for_assemble_burger_title()
            order_number = main_page.create_order_and_get_number()
            assert order_number is not None, "Номер заказа не получен"

        with allure.step("Шаг 3: Проверить, что счетчик 'Выполнено за всё время' увеличился"):
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)
            feed_page.wait_for_total_orders_to_increase(initial_total_orders)
            final_total_orders = feed_page.get_total_orders_count()
            assert final_total_orders > initial_total_orders, "Счетчик 'Выполнено за всё время' не увеличился"

    @allure.title("При создании заказа счетчик 'Выполнено за сегодня' увеличивается")
    def test_today_orders_counter_increases(self, logged_in_driver):
        """
        Проверяет, что после создания нового заказа счетчик "Выполнено за сегодня" увеличивается.
        """
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        with allure.step("Шаг 1: Получить начальное значение счетчика 'Выполнено за сегодня'"):
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)
            feed_page.wait_for_counters_to_load()
            initial_today_orders = feed_page.get_today_orders_count()

        with allure.step("Шаг 2: Создать новый заказ"):
            main_page.click_constructor_button()
            main_page.wait_for_assemble_burger_title()
            order_number = main_page.create_order_and_get_number()
            assert order_number is not None, "Номер заказа не получен"

        with allure.step("Шаг 3: Проверить, что счетчик 'Выполнено за сегодня' увеличился"):
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)
            feed_page.wait_for_today_orders_to_increase(initial_today_orders)
            final_today_orders = feed_page.get_today_orders_count()
            assert final_today_orders > initial_today_orders, "Счетчик 'Выполнено сегодня' не увеличился"

    @allure.title("После оформления заказа его номер появляется в разделе 'В работе'")
    def test_order_number_appears_in_progress(self, logged_in_driver):
        """
        Проверяет, что номер свежесозданного заказа появляется в разделе "В работе" на странице ленты заказов.
        """
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        with allure.step("Шаг 1: Создать новый заказ"):
            main_page.click_constructor_button()
            main_page.wait_for_assemble_burger_title()
            order_number = main_page.create_order_and_get_number()
            assert order_number is not None, "Номер заказа не получен"

        with allure.step("Шаг 2: Проверить, что номер заказа появился в разделе 'В работе'"):
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)
            feed_page.wait_for_order_in_progress(order_number)
            assert order_number in feed_page.get_in_progress_orders(), "Номер заказа не найден в ленте 'В работе'"
