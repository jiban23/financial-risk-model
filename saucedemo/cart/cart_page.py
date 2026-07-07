"""Locators and helpers for the SauceDemo Shopping Cart Module.

The test cases list https://www.saucedemo.com/v1/cart.html, but SauceDemo now
permanently redirects every /v1/ path to the current site, and the cart page
requires an authenticated session. These helpers log in, optionally add one or
more products, and open the cart, targeting the current (served) DOM.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://www.saucedemo.com/v1/"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

# --- Login / inventory locators ------------------------------------------
USERNAME = (By.ID, "user-name")
PASSWORD = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
INVENTORY_CONTAINER = (By.ID, "inventory_container")
ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

# --- Cart module ----------------------------------------------------------
CART_CONTAINER = (By.ID, "cart_contents_container")
CART_LIST = (By.CLASS_NAME, "cart_list")
CART_ITEM = (By.CLASS_NAME, "cart_item")
ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
ITEM_DESC = (By.CLASS_NAME, "inventory_item_desc")
ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")
REMOVE_BUTTONS = (By.CSS_SELECTOR, "button.cart_button")
CONTINUE_SHOPPING = (By.ID, "continue-shopping")
CHECKOUT_BUTTON = (By.ID, "checkout")
CHECKOUT_STEP_ONE = (By.ID, "checkout_info_container")


def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


def login(driver):
    driver.get(LOGIN_URL)
    wait(driver).until(EC.visibility_of_element_located(USERNAME)).send_keys(VALID_USER)
    driver.find_element(*PASSWORD).send_keys(VALID_PASS)
    driver.find_element(*LOGIN_BUTTON).click()
    wait(driver).until(EC.url_contains("inventory.html"))
    wait(driver).until(EC.visibility_of_element_located(INVENTORY_CONTAINER))


def add_products(driver, count):
    """Add the first ``count`` inventory products to the cart."""
    wait(driver).until(EC.element_to_be_clickable(ADD_TO_CART_BUTTONS))
    buttons = driver.find_elements(*ADD_TO_CART_BUTTONS)
    for button in buttons[:count]:
        button.click()


def open_cart(driver):
    driver.find_element(*CART_LINK).click()
    wait(driver).until(EC.url_contains("cart.html"))
    wait(driver).until(EC.visibility_of_element_located(CART_CONTAINER))


def open_empty_cart(driver):
    """Prerequisite: on the Cart page with no products added."""
    login(driver)
    open_cart(driver)


def open_cart_with(driver, count=1):
    """Prerequisite: on the Cart page with ``count`` product(s) added."""
    login(driver)
    add_products(driver, count)
    open_cart(driver)


def cart_items(driver):
    return driver.find_elements(*CART_ITEM)


def remove_buttons(driver):
    return driver.find_elements(*REMOVE_BUTTONS)
