"""Checkout Module test suite (CO-001 .. CO-032).

Covers the Checkout Information (step one), Order Summary / Overview (step two),
and Checkout Complete pages. Each test starts from the appropriate prerequisite
helper in ``checkout_page`` (a product is added and the flow is walked to the
page under test), since the checkout pages require an authenticated session.

Runs across every browser listed in ``--browsers`` (default: chrome, firefox,
edge, opera); unavailable browsers are SKIPPED rather than failed (see
./conftest.py, the driver factory in ../browsers.py, and options in
../conftest.py).
"""
from selenium.webdriver.support import expected_conditions as EC

import checkout_page as co


# ------------------------------------------------------------------ First Name
# CO-001 -- First Name field is displayed.
def test_co_001_first_name_display(driver):
    co.open_checkout_information(driver)
    assert driver.find_element(*co.FIRST_NAME).is_displayed()


# CO-002 -- First Name field accepts focus.
def test_co_002_first_name_focus(driver):
    co.open_checkout_information(driver)
    field = co.focus_field(driver, co.FIRST_NAME)
    assert driver.switch_to.active_element == field


# CO-003 -- Valid input can be entered into the First Name field.
def test_co_003_first_name_valid_input(driver):
    co.open_checkout_information(driver)
    field = co.enter_text(driver, co.FIRST_NAME, "John")
    assert field.get_attribute("value") == "John"


# CO-004 -- First Name left empty stays empty after moving focus away.
def test_co_004_first_name_empty(driver):
    co.open_checkout_information(driver)
    driver.find_element(*co.LAST_NAME).click()
    assert driver.find_element(*co.FIRST_NAME).get_attribute("value") == ""


# CO-005 -- Spaces can be entered into the First Name field.
def test_co_005_first_name_spaces(driver):
    co.open_checkout_information(driver)
    field = co.enter_text(driver, co.FIRST_NAME, "   ")
    assert field.get_attribute("value") == "   "


# ------------------------------------------------------------------- Last Name
# CO-006 -- Last Name field is displayed.
def test_co_006_last_name_display(driver):
    co.open_checkout_information(driver)
    assert driver.find_element(*co.LAST_NAME).is_displayed()


# CO-007 -- Last Name field accepts focus.
def test_co_007_last_name_focus(driver):
    co.open_checkout_information(driver)
    field = co.focus_field(driver, co.LAST_NAME)
    assert driver.switch_to.active_element == field


# CO-008 -- Valid input can be entered into the Last Name field.
def test_co_008_last_name_valid_input(driver):
    co.open_checkout_information(driver)
    field = co.enter_text(driver, co.LAST_NAME, "Doe")
    assert field.get_attribute("value") == "Doe"


# CO-009 -- Last Name left empty stays empty after moving focus away.
def test_co_009_last_name_empty(driver):
    co.open_checkout_information(driver)
    driver.find_element(*co.POSTAL_CODE).click()
    assert driver.find_element(*co.LAST_NAME).get_attribute("value") == ""


# CO-010 -- Spaces can be entered into the Last Name field.
def test_co_010_last_name_spaces(driver):
    co.open_checkout_information(driver)
    field = co.enter_text(driver, co.LAST_NAME, "   ")
    assert field.get_attribute("value") == "   "


# ----------------------------------------------------------------- Postal Code
# CO-011 -- Postal Code field is displayed.
def test_co_011_postal_code_display(driver):
    co.open_checkout_information(driver)
    assert driver.find_element(*co.POSTAL_CODE).is_displayed()


# CO-012 -- Postal Code field accepts focus.
def test_co_012_postal_code_focus(driver):
    co.open_checkout_information(driver)
    field = co.focus_field(driver, co.POSTAL_CODE)
    assert driver.switch_to.active_element == field


# CO-013 -- Valid input can be entered into the Postal Code field.
def test_co_013_postal_code_valid_input(driver):
    co.open_checkout_information(driver)
    field = co.enter_text(driver, co.POSTAL_CODE, "12345")
    assert field.get_attribute("value") == "12345"


# CO-014 -- Postal Code left empty stays empty after moving focus away.
def test_co_014_postal_code_empty(driver):
    co.open_checkout_information(driver)
    driver.find_element(*co.FIRST_NAME).click()
    assert driver.find_element(*co.POSTAL_CODE).get_attribute("value") == ""


# CO-015 -- Spaces can be entered into the Postal Code field.
def test_co_015_postal_code_spaces(driver):
    co.open_checkout_information(driver)
    field = co.enter_text(driver, co.POSTAL_CODE, "   ")
    assert field.get_attribute("value") == "   "


# ------------------------------------------------------------- Continue button
# CO-016 -- Continue button is displayed.
def test_co_016_continue_display(driver):
    co.open_checkout_information(driver)
    assert driver.find_element(*co.CONTINUE_BUTTON).is_displayed()


# CO-017 -- Valid information advances to the Order Summary page.
def test_co_017_continue_submit(driver):
    co.open_checkout_information(driver)
    co.fill_information(driver, co.VALID_FIRST, co.VALID_LAST, co.VALID_POSTAL)
    co.continue_checkout(driver)
    co.wait(driver).until(EC.url_contains("checkout-step-two.html"))
    assert driver.current_url.endswith("/checkout-step-two.html")


# CO-018 -- First Name empty shows the first-name-required error and icons.
def test_co_018_continue_first_name_empty(driver):
    co.open_checkout_information(driver)
    co.fill_information(driver, last=co.VALID_LAST, postal=co.VALID_POSTAL)
    co.continue_checkout(driver)
    assert co.error_text(driver) == co.ERR_FIRST_REQUIRED
    assert co.error_icon_count(driver) >= 1
    assert driver.current_url.endswith("/checkout-step-one.html")


# CO-019 -- Last Name empty shows the last-name-required error and icons.
def test_co_019_continue_last_name_empty(driver):
    co.open_checkout_information(driver)
    co.fill_information(driver, first=co.VALID_FIRST, postal=co.VALID_POSTAL)
    co.continue_checkout(driver)
    assert co.error_text(driver) == co.ERR_LAST_REQUIRED
    assert co.error_icon_count(driver) >= 1


# CO-020 -- Postal Code empty shows the postal-code-required error and icons.
def test_co_020_continue_postal_code_empty(driver):
    co.open_checkout_information(driver)
    co.fill_information(driver, first=co.VALID_FIRST, last=co.VALID_LAST)
    co.continue_checkout(driver)
    assert co.error_text(driver) == co.ERR_POSTAL_REQUIRED
    assert co.error_icon_count(driver) >= 1


# CO-021 -- All fields empty shows an error message and error icons.
def test_co_021_continue_all_empty(driver):
    co.open_checkout_information(driver)
    co.continue_checkout(driver)
    # SauceDemo validates first name first, so the first-name error is shown.
    assert co.error_text(driver) == co.ERR_FIRST_REQUIRED
    assert co.error_icon_count(driver) >= 1


# --------------------------------------------------------------- Cancel button
# CO-022 -- Cancel button is displayed.
def test_co_022_cancel_display(driver):
    co.open_checkout_information(driver)
    assert driver.find_element(*co.CANCEL_BUTTON).is_displayed()


# CO-023 -- Cancel returns to the Shopping Cart module.
def test_co_023_cancel_returns_to_cart(driver):
    co.open_checkout_information(driver)
    co.cancel_checkout(driver)
    co.wait(driver).until(EC.url_contains("cart.html"))
    assert driver.find_element(*co.CART_CONTAINER).is_displayed()


# ---------------------------------------------------------------- Order Summary
# CO-024 -- Order Summary page is displayed.
def test_co_024_order_summary_display(driver):
    co.open_order_summary(driver)
    assert driver.current_url.endswith("/checkout-step-two.html")
    assert co.wait(driver).until(
        EC.visibility_of_element_located(co.CART_ITEM)
    ).is_displayed()


# CO-025 -- Selected product information is displayed correctly.
def test_co_025_order_summary_product_info(driver):
    co.open_order_summary(driver)
    assert driver.find_element(*co.ITEM_NAME).text.strip()
    assert driver.find_element(*co.ITEM_DESC).text.strip()
    assert driver.find_element(*co.CART_QUANTITY).text == "1"
    assert driver.find_element(*co.ITEM_PRICE).text.startswith("$")


# CO-026 -- Payment information is displayed.
def test_co_026_order_summary_payment_info(driver):
    co.open_order_summary(driver)
    payment = driver.find_element(*co.PAYMENT_VALUE)
    assert payment.is_displayed()
    assert payment.text.strip()


# CO-027 -- Shipping information is displayed.
def test_co_027_order_summary_shipping_info(driver):
    co.open_order_summary(driver)
    shipping = driver.find_element(*co.SHIPPING_VALUE)
    assert shipping.is_displayed()
    assert shipping.text.strip()


# CO-028 -- Item total, tax and total are displayed and add up.
def test_co_028_order_summary_total(driver):
    co.open_order_summary(driver)
    subtotal = co.money(driver.find_element(*co.SUBTOTAL_LABEL).text)
    tax = co.money(driver.find_element(*co.TAX_LABEL).text)
    total = co.money(driver.find_element(*co.TOTAL_LABEL).text)
    item_price = co.money(driver.find_element(*co.ITEM_PRICE).text)
    assert subtotal == item_price
    assert round(subtotal + tax, 2) == total


# ---------------------------------------------------------------- Finish button
# CO-029 -- Finish button is displayed.
def test_co_029_finish_display(driver):
    co.open_order_summary(driver)
    assert driver.find_element(*co.FINISH_BUTTON).is_displayed()


# CO-030 -- Finish completes the order and shows the Checkout Complete page.
def test_co_030_finish_completes_order(driver):
    co.open_order_summary(driver)
    co.finish_order(driver)
    assert driver.current_url.endswith("/checkout-complete.html")
    assert "Thank you for your order" in driver.find_element(*co.COMPLETE_HEADER).text


# ------------------------------------------------------------- Back Home button
# CO-031 -- Back Home button is displayed on the Checkout Complete page.
def test_co_031_back_home_display(driver):
    co.open_checkout_complete(driver)
    assert driver.find_element(*co.BACK_HOME_BUTTON).is_displayed()


# CO-032 -- Back Home returns to the Inventory module.
def test_co_032_back_home_returns_to_inventory(driver):
    co.open_checkout_complete(driver)
    co.js_click(driver, driver.find_element(*co.BACK_HOME_BUTTON))
    co.wait(driver).until(EC.url_contains("inventory.html"))
    assert driver.find_element(*co.INVENTORY_CONTAINER).is_displayed()
