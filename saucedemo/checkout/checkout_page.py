"""Locators and helpers for the SauceDemo Checkout Module.

The test cases list https://www.saucedemo.com/v1/checkout-step-*.html URLs, but
SauceDemo now permanently redirects every /v1/ path to the current site, and the
checkout pages require an authenticated session with a product in the cart. These
helpers therefore log in, add a product, and walk into checkout, targeting the
current (served) DOM.

Note on input/click strategy: the checkout form fields and action buttons are
React-controlled. In this environment Selenium's synthesized keystrokes are
intermittently dropped before React commits them to state (so the field shows a
value the app never "sees"), and a native click on the submit button does not
fire the React handler. To keep the suite deterministic and cross-browser, text
is entered by setting the value through the native setter and dispatching a real
``input`` event (which React's onChange observes), and the Continue / Finish /
Cancel / Back Home buttons are activated with an element ``click()`` dispatched
via JavaScript. Both go through the same DOM APIs a real interaction would.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Entry point from the test-case prerequisites (redirects to the login page).
LOGIN_URL = "https://www.saucedemo.com/v1/"

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

# Valid checkout information used by the happy-path cases.
VALID_FIRST = "John"
VALID_LAST = "Doe"
VALID_POSTAL = "12345"

# --- Login / navigation locators -----------------------------------------
USERNAME = (By.ID, "user-name")
PASSWORD = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
CART_CONTAINER = (By.ID, "cart_contents_container")
CHECKOUT_BUTTON = (By.ID, "checkout")
PAGE_TITLE = (By.CLASS_NAME, "title")
INVENTORY_CONTAINER = (By.ID, "inventory_container")

# --- Checkout: Your Information (step one) --------------------------------
FIRST_NAME = (By.ID, "first-name")
LAST_NAME = (By.ID, "last-name")
POSTAL_CODE = (By.ID, "postal-code")
CONTINUE_BUTTON = (By.ID, "continue")
CANCEL_BUTTON = (By.ID, "cancel")
ERROR = (By.CSS_SELECTOR, "[data-test='error']")
ERROR_ICON = (By.CSS_SELECTOR, ".error_icon")

# --- Checkout: Overview (step two / order summary) ------------------------
CART_ITEM = (By.CLASS_NAME, "cart_item")
ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
ITEM_DESC = (By.CLASS_NAME, "inventory_item_desc")
ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
CART_QUANTITY = (By.CLASS_NAME, "cart_quantity")
SUMMARY_INFO_LABEL = (By.CLASS_NAME, "summary_info_label")
PAYMENT_VALUE = (By.CSS_SELECTOR, "[data-test='payment-info-value']")
SHIPPING_VALUE = (By.CSS_SELECTOR, "[data-test='shipping-info-value']")
SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
FINISH_BUTTON = (By.ID, "finish")

# --- Checkout: Complete ---------------------------------------------------
COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
BACK_HOME_BUTTON = (By.ID, "back-to-products")

# Error strings SauceDemo returns (verified against the live site).
ERR_FIRST_REQUIRED = "Error: First Name is required"
ERR_LAST_REQUIRED = "Error: Last Name is required"
ERR_POSTAL_REQUIRED = "Error: Postal Code is required"

# Sets an input's value through the native setter and fires a real ``input``
# event so React's onChange handler commits the value to component state.
_JS_SET_VALUE = (
    "const setter = Object.getOwnPropertyDescriptor("
    "window.HTMLInputElement.prototype, 'value').set;"
    "setter.call(arguments[0], arguments[1]);"
    "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
)


def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


def js_click(driver, element):
    driver.execute_script("arguments[0].click();", element)


def enter_text(driver, locator, text):
    """Type ``text`` into the field at ``locator`` (React-safe) and return it."""
    field = wait(driver).until(EC.visibility_of_element_located(locator))
    driver.execute_script(_JS_SET_VALUE, field, text)
    return field


def focus_field(driver, locator):
    """Click the field and wait until it is the focused element; return it."""
    field = wait(driver).until(EC.element_to_be_clickable(locator))
    field.click()
    wait(driver).until(lambda d: d.switch_to.active_element == field)
    return field


def login(driver):
    driver.get(LOGIN_URL)
    wait(driver).until(EC.visibility_of_element_located(USERNAME)).send_keys(VALID_USER)
    driver.find_element(*PASSWORD).send_keys(VALID_PASS)
    driver.find_element(*LOGIN_BUTTON).click()
    wait(driver).until(EC.url_contains("inventory.html"))
    wait(driver).until(EC.visibility_of_element_located(INVENTORY_CONTAINER))


def open_checkout_information(driver):
    """Prerequisite: on the Checkout Information page with one product added."""
    login(driver)
    wait(driver).until(EC.element_to_be_clickable(ADD_TO_CART_BUTTONS))
    driver.find_elements(*ADD_TO_CART_BUTTONS)[0].click()
    driver.find_element(*CART_LINK).click()
    wait(driver).until(EC.url_contains("cart.html"))
    wait(driver).until(EC.element_to_be_clickable(CHECKOUT_BUTTON)).click()
    wait(driver).until(EC.url_contains("checkout-step-one.html"))
    wait(driver).until(EC.visibility_of_element_located(FIRST_NAME))


def fill_information(driver, first=None, last=None, postal=None):
    """Fill only the fields whose value is provided (non-None)."""
    if first is not None:
        enter_text(driver, FIRST_NAME, first)
    if last is not None:
        enter_text(driver, LAST_NAME, last)
    if postal is not None:
        enter_text(driver, POSTAL_CODE, postal)


def continue_checkout(driver):
    js_click(driver, driver.find_element(*CONTINUE_BUTTON))


def cancel_checkout(driver):
    js_click(driver, driver.find_element(*CANCEL_BUTTON))


def open_order_summary(driver):
    """Prerequisite: on the Order Summary (Overview) page for one product."""
    open_checkout_information(driver)
    fill_information(driver, VALID_FIRST, VALID_LAST, VALID_POSTAL)
    continue_checkout(driver)
    wait(driver).until(EC.url_contains("checkout-step-two.html"))


def finish_order(driver):
    js_click(driver, driver.find_element(*FINISH_BUTTON))
    wait(driver).until(EC.url_contains("checkout-complete.html"))


def open_checkout_complete(driver):
    """Prerequisite: on the Checkout Complete page after finishing an order."""
    open_order_summary(driver)
    finish_order(driver)


def error_text(driver):
    return wait(driver).until(EC.visibility_of_element_located(ERROR)).text


def error_icon_count(driver):
    return len(driver.find_elements(*ERROR_ICON))


def money(text):
    """Extract the numeric amount from a label like 'Item total: $29.99'."""
    return float(text.split("$")[1])
