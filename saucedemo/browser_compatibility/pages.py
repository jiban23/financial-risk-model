"""Locators and small helpers for the SauceDemo site.

NOTE: the test cases list https://www.saucedemo.com/v1/ URLs, but SauceDemo now
permanently redirects every /v1/ path to the current site. These locators target
the current (served) DOM. Using the /v1/ login URL as the entry point still works
because it redirects to the login page.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Entry point from the test-case prerequisites (redirects to the login page).
LOGIN_URL = "https://www.saucedemo.com/v1/"
INVENTORY_URL = "https://www.saucedemo.com/inventory.html"
CART_URL = "https://www.saucedemo.com/cart.html"
CHECKOUT_STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"

STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"

# --- Locators -------------------------------------------------------------
USERNAME = (By.ID, "user-name")
PASSWORD_FIELD = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")

PAGE_TITLE = (By.CLASS_NAME, "title")
INVENTORY_CONTAINER = (By.ID, "inventory_container")
INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

CART_CONTAINER = (By.ID, "cart_contents_container")
CART_ITEM = (By.CLASS_NAME, "cart_item")
CHECKOUT_BUTTON = (By.ID, "checkout")

FIRST_NAME = (By.ID, "first-name")
LAST_NAME = (By.ID, "last-name")
POSTAL_CODE = (By.ID, "postal-code")
CONTINUE_BUTTON = (By.ID, "continue")
FINISH_BUTTON = (By.ID, "finish")
COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

MENU_BUTTON = (By.ID, "react-burger-menu-btn")
MENU_ITEMS = {
    "All Items": (By.ID, "inventory_sidebar_link"),
    "About": (By.ID, "about_sidebar_link"),
    "Logout": (By.ID, "logout_sidebar_link"),
    "Reset App State": (By.ID, "reset_sidebar_link"),
}


# --- Helpers --------------------------------------------------------------
def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


def visible(driver, locator, timeout=10):
    return wait(driver, timeout).until(EC.visibility_of_element_located(locator))


def login(driver, username=STANDARD_USER, password=PASSWORD):
    driver.get(LOGIN_URL)
    visible(driver, USERNAME).send_keys(username)
    driver.find_element(*PASSWORD_FIELD).send_keys(password)
    driver.find_element(*LOGIN_BUTTON).click()
    wait(driver).until(EC.url_contains("inventory.html"))


def add_first_item_and_open_cart(driver):
    """Log in, add the first product, and land on the cart page."""
    login(driver)
    driver.find_elements(*ADD_TO_CART_BUTTONS)[0].click()
    driver.find_element(*CART_LINK).click()
    wait(driver).until(EC.url_contains("cart.html"))
