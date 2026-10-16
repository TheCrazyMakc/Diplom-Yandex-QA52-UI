from selenium.webdriver.common.by import By


class MainPageLocators:
    """
    Локаторы для главной страницы (конструктор бургеров).
    """
    MODAL_CLOSE_BUTTON = (
        By.XPATH,
        ".//section[contains(@class, 'Modal_modal_opened__') and"
        " contains(@class, 'Modal_modal__')]//button[contains(@class, 'Modal_modal__close_modified')]"
    )
    MODAL_OPENED = (
        By.XPATH,
        ".//section[contains(@class, 'Modal_modal_opened__') and contains(@class, 'Modal_modal__')]"
    )
    MODAL_HEADER_OPENED = (
        By.XPATH,
        ".//section[contains(@class, 'Modal_modal_opened__') and "
        "contains(@class, 'Modal_modal__')]//h2[text()='Детали ингредиента']"
    )
    ORDER_MODAL_OPENED = (
        By.XPATH,
        ".//section[contains(@class, 'Modal_modal_opened__')]//p[text()='Ваш заказ начали готовить']"
    )
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title')]")

    BURGER_CONSTRUCTOR_AREA = (By.XPATH, ".//ul[@class='BurgerConstructor_basket__list__l9dp_']")

    INGREDIENT_COUNTER = (By.XPATH, ".//p[@class='counter_counter__num__3nue1']")

    FIRST_BUN = (By.XPATH, "//h2[text()='Булки']/following-sibling::ul[1]/a[1]")
    FIRST_SAUCE = (By.XPATH, "//h2[text()='Соусы']/following-sibling::ul[1]/a[1]")
    FIRST_FILLING = (By.XPATH, "//h2[text()='Начинки']/following-sibling::ul[1]/a[1]")

    FIRST_BUN_COUNTER = (By.XPATH, "(//h2[text()='Булки']/following-sibling::ul//p[contains(@class, 'counter_counter__num__3nue1')])[1]")
    FIRST_SAUCE_COUNTER = (By.XPATH, "(//h2[text()='Соусы']/following-sibling::ul//p[contains(@class, 'counter_counter__num__3nue1')])[1]")
    FIRST_FILLING_COUNTER = (By.XPATH, "(//h2[text()='Начинки']/following-sibling::ul//p[contains(@class, 'counter_counter__num__3nue1')])[1]")

    ASSEMBLE_BURGER_TITLE = (By.XPATH, ".//h1[text()='Соберите бургер']")

    ORDER_FEED_BUTTON = (By.XPATH, ".//p[text()='Лента Заказов']")
    CONSTRUCTOR_BUTTON = (By.XPATH, ".//p[text()='Конструктор']")
    PLACE_ORDER_BUTTON = (By.XPATH, ".//button[text()='Оформить заказ']")
