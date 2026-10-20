from selenium.webdriver.common.by import By


class FeedPageLocators:
    """
    Локаторы для страницы ленты заказов.
    """
    TOTAL_ORDERS_COUNTER = (
        By.XPATH,
        ".//div[p[text()='Выполнено за все время:']]/p[contains(@class, 'OrderFeed_number__2MbrQ')]"
    )
    TODAY_ORDERS_COUNTER = (
        By.XPATH,
        ".//div[p[text()='Выполнено за сегодня:']]/p[contains(@class, 'OrderFeed_number__2MbrQ')]"
    )
    IN_PROGRESS_ORDERS = (
        By.XPATH,
        "//ul[@class='OrderFeed_orderListReady__1YFem OrderFeed_orderList__cBvyi']/li[contains(@class,'text_type_digits-default')]"
    )
