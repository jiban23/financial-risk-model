"""Locators and helpers for the SauceDemo UI / visual test suite.

The UI test cases list https://www.saucedemo.com/v1/ (login) and
https://www.saucedemo.com/v1/inventory.html (inventory) as URLs; SauceDemo now
permanently redirects every /v1/ path to the current site, so these locators
target the current (served) DOM -- consistent with ../login/login_page.py and
../inventory/inventory_page.py.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://www.saucedemo.com/v1/"
CART_URL = "https://www.saucedemo.com/cart.html"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

# --- Login page ----------------------------------------------------------
LOGIN_LOGO = (By.CLASS_NAME, "login_logo")
USERNAME = (By.ID, "user-name")
PASSWORD = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
ERROR = (By.CSS_SELECTOR, "[data-test='error']")
ERROR_ICON = (By.CSS_SELECTOR, ".error_icon")

# --- Inventory / shared chrome -------------------------------------------
APP_LOGO = (By.CLASS_NAME, "app_logo")
PAGE_TITLE = (By.CLASS_NAME, "title")
INVENTORY_CONTAINER = (By.ID, "inventory_container")
INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
ITEM_IMG = (By.CSS_SELECTOR, ".inventory_item_img img")
ADD_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
FOOTER = (By.CSS_SELECTOR, "footer")
FOOTER_COPY = (By.CLASS_NAME, "footer_copy")

MENU_BUTTON = (By.ID, "react-burger-menu-btn")
MENU_WRAP = (By.CLASS_NAME, "bm-menu-wrap")
MENU_ITEM_LOCATORS = {
    "All Items": (By.ID, "inventory_sidebar_link"),
    "About": (By.ID, "about_sidebar_link"),
    "Logout": (By.ID, "logout_sidebar_link"),
    "Reset App State": (By.ID, "reset_sidebar_link"),
}

EXPECTED_ITEM_COUNT = 6


# --- Helpers -------------------------------------------------------------
def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


def open_login(driver):
    driver.get(LOGIN_URL)
    wait(driver).until(EC.visibility_of_element_located(USERNAME))


def login_to_inventory(driver):
    driver.get(LOGIN_URL)
    wait(driver).until(EC.visibility_of_element_located(USERNAME)).send_keys(VALID_USER)
    driver.find_element(*PASSWORD).send_keys(VALID_PASS)
    driver.find_element(*LOGIN_BUTTON).click()
    wait(driver).until(EC.url_contains("inventory.html"))
    wait(driver).until(EC.visibility_of_element_located(INVENTORY_CONTAINER))


def open_menu(driver):
    """Open the burger navigation menu and wait for its items to be clickable."""
    driver.find_element(*MENU_BUTTON).click()
    wait(driver).until(
        EC.element_to_be_clickable(MENU_ITEM_LOCATORS["All Items"])
    )


def trigger_login_error(driver):
    """Submit invalid credentials so the error banner is rendered."""
    open_login(driver)
    driver.find_element(*USERNAME).send_keys("invalid_user")
    driver.find_element(*PASSWORD).send_keys("wrong_pass")
    driver.find_element(*LOGIN_BUTTON).click()
    return wait(driver).until(EC.visibility_of_element_located(ERROR))


def css_value(driver, element, prop):
    """Computed CSS value of *prop* for *element* (e.g. 'font-family')."""
    return driver.execute_script(
        "return window.getComputedStyle(arguments[0]).getPropertyValue(arguments[1]);",
        element,
        prop,
    ).strip()


def image_loaded(driver, img):
    """True when an <img> actually rendered (naturalWidth > 0 = not broken)."""
    return driver.execute_script("return arguments[0].naturalWidth;", img) > 0


def wait_images_loaded(driver, count):
    """Wait until *count* product images have finished decoding.

    Right after login the <img> elements exist but may not have loaded yet
    (notably in headless Edge), so ``is_displayed()`` can transiently be False.
    Gating on ``complete && naturalWidth > 0`` removes that race.
    """
    wait(driver).until(
        lambda d: len(d.find_elements(*ITEM_IMG)) == count
        and all(
            d.execute_script("return arguments[0].complete && arguments[0].naturalWidth > 0;", i)
            for i in d.find_elements(*ITEM_IMG)
        )
    )


def rects_overlap(a, b):
    """True when two Selenium ``.rect`` dicts overlap (share screen area)."""
    return not (
        a["x"] + a["width"] <= b["x"]
        or b["x"] + b["width"] <= a["x"]
        or a["y"] + a["height"] <= b["y"]
        or b["y"] + b["height"] <= a["y"]
    )
