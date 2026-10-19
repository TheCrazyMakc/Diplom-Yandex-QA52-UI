from selenium.webdriver.common.by import By

class BaseLocators:
    MODAL_OVERLAY = (By.XPATH, ".//div[contains(@class, 'Modal_modal_overlay__')]")