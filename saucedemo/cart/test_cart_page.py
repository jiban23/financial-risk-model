"""Shopping Cart Module test suite (SC-001 .. SC-016).

Covers the display of the cart, added-product details (name, description,
price, quantity), single and multiple products, the Remove / Continue Shopping
/ Checkout controls, and the empty-cart checkout behaviour. Each test starts
from the appropriate prerequisite helper in ``cart_page`` (login + optionally
add products + open the cart), since the cart page requires an authenticated
session.

Runs across every browser listed in ``--browsers`` (default: chrome, firefox,
edge, opera); unavailable browsers are SKIPPED rather than failed (see
./conftest.py, the driver factory in ../browsers.py, and options in
../conftest.py).
"""
from selenium.webdriver.support import expected_conditions as EC

import cart_page as cart


# ------------------------------------------------------------------ Display
# SC-001 -- Shopping Cart module is displayed.
def test_sc_001_cart_display(driver):
    cart.open_empty_cart(driver)
    assert driver.find_element(*cart.CART_CONTAINER).is_displayed()


# SC-002 -- Empty cart: module is displayed without any products.
def test_sc_002_empty_cart(driver):
    cart.open_empty_cart(driver)
    assert driver.find_element(*cart.CART_CONTAINER).is_displayed()
    assert cart.cart_items(driver) == []


# SC-003 -- Added product is displayed in the cart.
def test_sc_003_added_product_displayed(driver):
    cart.open_cart_with(driver, 1)
    assert len(cart.cart_items(driver)) == 1


# ------------------------------------------------------------ Product details
# SC-004 -- Added product name is displayed.
def test_sc_004_product_name(driver):
    cart.open_cart_with(driver, 1)
    assert driver.find_element(*cart.ITEM_NAME).text.strip()


# SC-005 -- Added product description is displayed.
def test_sc_005_product_description(driver):
    cart.open_cart_with(driver, 1)
    assert driver.find_element(*cart.ITEM_DESC).text.strip()


# SC-006 -- Added product price is displayed.
def test_sc_006_product_price(driver):
    cart.open_cart_with(driver, 1)
    price = driver.find_element(*cart.ITEM_PRICE)
    assert price.is_displayed()
    assert price.text.startswith("$")


# SC-007 -- Added product quantity is displayed.
def test_sc_007_product_quantity(driver):
    cart.open_cart_with(driver, 1)
    quantity = driver.find_element(*cart.CART_QUANTITY)
    assert quantity.is_displayed()
    assert quantity.text == "1"


# SC-008 -- Multiple added products are displayed.
def test_sc_008_multiple_products(driver):
    cart.open_cart_with(driver, 3)
    assert len(cart.cart_items(driver)) == 3


# --------------------------------------------------------------- Remove product
# SC-009 -- Remove button is displayed.
def test_sc_009_remove_button_display(driver):
    cart.open_cart_with(driver, 1)
    assert driver.find_element(*cart.REMOVE_BUTTONS).is_displayed()


# SC-010 -- An added product can be removed from the cart.
def test_sc_010_remove_product(driver):
    cart.open_cart_with(driver, 1)
    assert len(cart.cart_items(driver)) == 1
    cart.remove_buttons(driver)[0].click()
    cart.wait(driver).until(lambda d: len(cart.cart_items(d)) == 0)
    assert cart.cart_items(driver) == []


# SC-011 -- All added products can be removed from the cart.
def test_sc_011_remove_all_products(driver):
    cart.open_cart_with(driver, 3)
    assert len(cart.cart_items(driver)) == 3
    while cart.remove_buttons(driver):
        before = len(cart.cart_items(driver))
        cart.remove_buttons(driver)[0].click()
        cart.wait(driver).until(lambda d, n=before: len(cart.cart_items(d)) < n)
    assert cart.cart_items(driver) == []


# ----------------------------------------------------- Continue Shopping button
# SC-012 -- Continue Shopping button is displayed.
def test_sc_012_continue_shopping_display(driver):
    cart.open_empty_cart(driver)
    assert driver.find_element(*cart.CONTINUE_SHOPPING).is_displayed()


# SC-013 -- Continue Shopping returns to the Inventory module.
def test_sc_013_continue_shopping_returns_to_inventory(driver):
    cart.open_empty_cart(driver)
    driver.find_element(*cart.CONTINUE_SHOPPING).click()
    cart.wait(driver).until(EC.url_contains("inventory.html"))
    assert driver.find_element(*cart.INVENTORY_CONTAINER).is_displayed()


# ------------------------------------------------------------- Checkout button
# SC-014 -- Checkout button is displayed.
def test_sc_014_checkout_button_display(driver):
    cart.open_empty_cart(driver)
    assert driver.find_element(*cart.CHECKOUT_BUTTON).is_displayed()


# SC-015 -- Checkout button proceeds to the Checkout module.
def test_sc_015_checkout_proceeds(driver):
    cart.open_cart_with(driver, 1)
    driver.find_element(*cart.CHECKOUT_BUTTON).click()
    cart.wait(driver).until(EC.url_contains("checkout-step-one.html"))
    assert driver.find_element(*cart.CHECKOUT_STEP_ONE).is_displayed()


# SC-016 -- Empty-cart checkout should be prevented (business expectation).
# Expected: the app blocks checkout and warns that no products are selected.
# Actual SauceDemo behaviour: it proceeds to Checkout Information with an empty
# cart and shows no warning -- recorded here as a defect (this test FAILS).
def test_sc_016_empty_cart_checkout_blocked(driver):
    cart.open_empty_cart(driver)
    driver.find_element(*cart.CHECKOUT_BUTTON).click()
    cart.wait(driver).until(
        lambda d: "checkout-step-one.html" in d.current_url
        or "cart.html" in d.current_url
    )
    assert "cart.html" in driver.current_url, (
        "SauceDemo allows checkout with an empty cart (no warning shown) — "
        "expected the app to prevent empty-cart checkout"
    )
