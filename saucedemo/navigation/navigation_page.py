"""Locators and helpers for the SauceDemo navigation (burger) menu.

The test cases list https://www.saucedemo.com/v1/inventory.html; SauceDemo
redirects /v1/ to the current site, and the menu is only reachable from an
authenticated session, so helpers log in first.

The v1 menu is built with react-burger-menu: the links live in the DOM even
while the panel is closed, so "displayed" checks wait for the panel to slide
open (``.bm-menu-wrap`` toggles ``aria-hidden`` false) before asserting.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://www.saucedemo.com/v1/"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"
ABOUT_URL = "saucelabs.com"

USERNAME = (By.ID, "user-name")
PASSWORD = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")

INVENTORY_CONTAINER = (By.ID, "inventory_container")
ADD_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
REMOVE_BUTTONS = (By.CSS_SELECTOR, "button.btn_secondary")
CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

MENU_BUTTON = (By.CSS_SELECTOR, ".bm-burger-button")
MENU_WRAP = (By.CLASS_NAME, "bm-menu-wrap")
ALL_ITEMS_LINK = (By.ID, "inventory_sidebar_link")
ABOUT_LINK = (By.ID, "about_sidebar_link")
RESET_LINK = (By.ID, "reset_sidebar_link")
LOGOUT_LINK = (By.ID, "logout_sidebar_link")


def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


def login_to_inventory(driver):
    driver.get(LOGIN_URL)
    wait(driver).until(EC.visibility_of_element_located(USERNAME)).send_keys(VALID_USER)
    driver.find_element(*PASSWORD).send_keys(VALID_PASS)
    driver.find_element(*LOGIN_BUTTON).click()
    wait(driver).until(EC.url_contains("inventory.html"))
    wait(driver).until(EC.visibility_of_element_located(INVENTORY_CONTAINER))


def open_menu(driver):
    """Click the burger button and wait for the panel to finish sliding open.

    react-burger-menu flips ``aria-hidden`` on the wrap immediately but keeps
    the panel/links invisible until the CSS slide animation finishes, so we
    wait on link visibility -- the reliable "panel is really open" signal.
    """
    driver.find_element(*MENU_BUTTON).click()
    wait(driver).until(EC.visibility_of_element_located(ALL_ITEMS_LINK))


def menu_is_open(driver):
    """True once the panel has finished opening (a link is visible)."""
    links = driver.find_elements(*ALL_ITEMS_LINK)
    return bool(links) and links[0].is_displayed()


def click_menu_link(driver, locator):
    """Activate a menu item with a JS click.

    react-burger-menu's slide overlay intercepts Selenium's native click while
    the panel is animating, so a normal ``.click()`` is swallowed and no
    navigation happens. A JS click fires directly on the anchor and reliably
    triggers its action -- the standard technique for animated menus.
    """
    driver.execute_script("arguments[0].click();", driver.find_element(*locator))


def add_first_product(driver):
    driver.find_element(*ADD_BUTTONS).click()
    wait(driver).until(EC.visibility_of_element_located(CART_BADGE))


def badge_count(driver):
    """Return the cart badge number, or 0 when no badge is shown."""
    badges = driver.find_elements(*CART_BADGE)
    return int(badges[0].text) if badges and badges[0].text.strip() else 0
