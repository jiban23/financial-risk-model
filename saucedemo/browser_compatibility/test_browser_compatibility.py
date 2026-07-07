"""Browser compatibility test suite (BC-001 .. BC-007).

Each test runs once per browser selected via --browsers (chrome, edge, firefox,
opera); unavailable browsers are skipped. Display-oriented cases also save a
screenshot under browser_compatibility/screenshots/ for manual layout review,
since "renders without layout issues" cannot be fully asserted programmatically.
"""
import os
import pytest
from selenium.webdriver.support import expected_conditions as EC

import pages

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


def _shot(driver, case):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, f"{case}_{driver.browser_name}.png")
    driver.save_screenshot(path)


# BC-001 -- Application Access: the login module loads in each browser.
def test_bc_001_application_access(driver):
    driver.get(pages.LOGIN_URL)
    assert pages.visible(driver, pages.USERNAME).is_displayed()
    assert driver.find_element(*pages.PASSWORD_FIELD).is_displayed()
    assert driver.find_element(*pages.LOGIN_BUTTON).is_displayed()
    _shot(driver, "BC-001")


# BC-002 -- Login: valid credentials land on the inventory module.
def test_bc_002_login(driver):
    pages.login(driver)
    assert driver.current_url.endswith("/inventory.html")
    assert pages.visible(driver, pages.PAGE_TITLE).text == "Products"


# BC-003 -- Inventory display: container and products render.
def test_bc_003_inventory_display(driver):
    pages.login(driver)
    assert pages.visible(driver, pages.INVENTORY_CONTAINER).is_displayed()
    assert pages.visible(driver, pages.PAGE_TITLE).text == "Products"
    assert len(driver.find_elements(*pages.INVENTORY_ITEM)) == 6
    _shot(driver, "BC-003")


# BC-004 -- Shopping cart display: cart renders with the added product.
def test_bc_004_cart_display(driver):
    pages.add_first_item_and_open_cart(driver)
    assert pages.visible(driver, pages.CART_CONTAINER).is_displayed()
    assert pages.visible(driver, pages.PAGE_TITLE).text == "Your Cart"
    assert len(driver.find_elements(*pages.CART_ITEM)) == 1
    _shot(driver, "BC-004")


# BC-005 -- Checkout display: the checkout information page renders its fields.
def test_bc_005_checkout_display(driver):
    pages.add_first_item_and_open_cart(driver)
    driver.find_element(*pages.CHECKOUT_BUTTON).click()
    pages.wait(driver).until(EC.url_contains("checkout-step-one.html"))
    assert pages.visible(driver, pages.PAGE_TITLE).text == "Checkout: Your Information"
    assert driver.find_element(*pages.FIRST_NAME).is_displayed()
    assert driver.find_element(*pages.LAST_NAME).is_displayed()
    assert driver.find_element(*pages.POSTAL_CODE).is_displayed()
    _shot(driver, "BC-005")


# BC-006 -- Navigation menu: all menu options are present and accessible.
def test_bc_006_navigation_menu(driver):
    pages.login(driver)
    driver.find_element(*pages.MENU_BUTTON).click()
    for label, locator in pages.MENU_ITEMS.items():
        element = pages.visible(driver, locator)
        assert element.is_displayed(), f"Menu item '{label}' not visible"
    _shot(driver, "BC-006")


# BC-007 -- Overall compatibility: full purchase flow works end to end.
def test_bc_007_overall_compatibility(driver):
    pages.add_first_item_and_open_cart(driver)
    driver.find_element(*pages.CHECKOUT_BUTTON).click()
    pages.visible(driver, pages.FIRST_NAME).send_keys("Miguel")
    driver.find_element(*pages.LAST_NAME).send_keys("Tester")
    driver.find_element(*pages.POSTAL_CODE).send_keys("1000")
    driver.find_element(*pages.CONTINUE_BUTTON).click()
    pages.wait(driver).until(EC.url_contains("checkout-step-two.html"))
    driver.find_element(*pages.FINISH_BUTTON).click()
    pages.wait(driver).until(EC.url_contains("checkout-complete.html"))
    assert "Thank you for your order" in pages.visible(driver, pages.COMPLETE_HEADER).text
