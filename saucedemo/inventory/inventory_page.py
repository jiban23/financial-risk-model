"""Locators and helpers for the SauceDemo Inventory Module.

The test cases list https://www.saucedemo.com/v1/inventory.html; SauceDemo
redirects /v1/ to the current site, and the inventory page requires an
authenticated session, so helpers log in first.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://www.saucedemo.com/v1/"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

USERNAME = (By.ID, "user-name")
PASSWORD = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")

INVENTORY_CONTAINER = (By.ID, "inventory_container")
INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
ITEM_DESC = (By.CLASS_NAME, "inventory_item_desc")
ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
ITEM_IMG = (By.CSS_SELECTOR, ".inventory_item_img img")
ADD_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
REMOVE_BUTTONS = (By.CSS_SELECTOR, "button.btn_secondary")
CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
SORT_SELECT = (By.CLASS_NAME, "product_sort_container")

EXPECTED_ITEM_COUNT = 6
LONGEST_NAME = "Test.allTheThings() T-Shirt (Red)"


def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


def login_to_inventory(driver):
    driver.get(LOGIN_URL)
    wait(driver).until(EC.visibility_of_element_located(USERNAME)).send_keys(VALID_USER)
    driver.find_element(*PASSWORD).send_keys(VALID_PASS)
    driver.find_element(*LOGIN_BUTTON).click()
    wait(driver).until(EC.url_contains("inventory.html"))
    wait(driver).until(EC.visibility_of_element_located(INVENTORY_CONTAINER))


def add_buttons(driver):
    return driver.find_elements(*ADD_BUTTONS)


def badge_count(driver):
    """Return the cart badge number, or 0 when no badge is shown."""
    badges = driver.find_elements(*CART_BADGE)
    return int(badges[0].text) if badges and badges[0].text.strip() else 0


def prices(driver):
    return [float(e.text.replace("$", "")) for e in driver.find_elements(*ITEM_PRICE)]


def names(driver):
    return [e.text for e in driver.find_elements(*ITEM_NAME)]


def select_sort(driver, value):
    Select(driver.find_element(*SORT_SELECT)).select_by_value(value)
