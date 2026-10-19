from pages.main_page import MainPage
from pages.feed_page import FeedPage
from data.urls import Urls
import allure
from utils.text import normalize_order_number


@allure.suite("Лента заказов")
class TestOrderFeed:
    """
    Тесты для проверки функциональности ленты заказов.

    Каждый тест проверяет ровно одно поведение приложения.
    Создание заказа вынесено в фикстуру created_order (Arrange),
    ассерт всегда стоит последним шагом теста.
    """

    @allure.title("При создании заказа счетчик 'Выполнено за все время' увеличивается")
    def test_total_orders_counter_increases(self, logged_in_driver):
        """
        Проверяет, что после создания нового заказа счетчик
        "Выполнено за всё время" увеличивается.
        """
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        with allure.step("Arrange: зафиксировать начальное значение счетчика 'Выполнено за всё время'"):
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)
            feed_page.wait_for_counters_to_load()
            initial_total_orders = feed_page.get_total_orders_count()

        with allure.step("Act: создать новый заказ и вернуться в ленту заказов"):
            main_page.click_constructor_button()
            main_page.wait_for_assemble_burger_title()
            main_page.create_order_and_get_number()
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)

        with allure.step("Assert: счетчик 'Выполнено за всё время' увеличился"):
            feed_page.wait_for_total_orders_to_increase(initial_total_orders)
            final_total_orders = feed_page.get_total_orders_count()
            assert final_total_orders > initial_total_orders, (
                "Счетчик 'Выполнено за всё время' не увеличился: "
                f"было {initial_total_orders}, стало {final_total_orders}"
            )

    @allure.title("При создании заказа счетчик 'Выполнено за сегодня' увеличивается")
    def test_today_orders_counter_increases(self, logged_in_driver):
        """
        Проверяет, что после создания нового заказа счетчик
        "Выполнено за сегодня" увеличивается.
        """
        main_page = MainPage(logged_in_driver)
        feed_page = FeedPage(logged_in_driver)

        with allure.step("Arrange: зафиксировать начальное значение счетчика 'Выполнено за сегодня'"):
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)
            feed_page.wait_for_counters_to_load()
            initial_today_orders = feed_page.get_today_orders_count()

        with allure.step("Act: создать новый заказ и вернуться в ленту заказов"):
            main_page.click_constructor_button()
            main_page.wait_for_assemble_burger_title()
            main_page.create_order_and_get_number()
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)

        with allure.step("Assert: счетчик 'Выполнено за сегодня' увеличился"):
            feed_page.wait_for_today_orders_to_increase(initial_today_orders)
            final_today_orders = feed_page.get_today_orders_count()
            assert final_today_orders > initial_today_orders, (
                "Счетчик 'Выполнено за сегодня' не увеличился: "
                f"было {initial_today_orders}, стало {final_today_orders}"
            )

    @allure.title("После оформления заказа его номер появляется в разделе 'В работе'")
    def test_order_number_appears_in_progress(self, created_order):
        """
        Проверяет, что номер свежесозданного заказа появляется
        в разделе "В работе" на странице ленты заказов.
        """
        driver, order_number = created_order
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)

        with allure.step("Act: открыть ленту заказов"):
            main_page.click_order_feed_button()
            feed_page.wait_for_url_to_be(Urls.FEED_URL)

        with allure.step("Assert: номер заказа появился в разделе 'В работе'"):
            feed_page.wait_for_order_in_progress(order_number)
            in_progress_orders = feed_page.get_in_progress_orders()
            assert normalize_order_number(order_number) in in_progress_orders, (
                f"Номер заказа {order_number} не найден в разделе 'В работе'. "
                f"Текущий список: {in_progress_orders}"
            )