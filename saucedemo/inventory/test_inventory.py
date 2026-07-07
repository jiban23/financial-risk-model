"""Inventory Module test suite (INV-001 .. INV-019), Google Chrome only.

Uses the repo-root Chrome ``driver`` fixture (see ../conftest.py). Each test
logs in first, since the inventory page requires an authenticated session.
"""
from selenium.webdriver.support import expected_conditions as EC

import inventory_page as inv


# INV-001 -- Product list is displayed.
def test_inv_001_product_list_display(driver):
    inv.login_to_inventory(driver)
    assert driver.find_element(*inv.INVENTORY_CONTAINER).is_displayed()
    assert len(driver.find_elements(*inv.INVENTORY_ITEM)) == inv.EXPECTED_ITEM_COUNT


# INV-002 -- Product names are displayed.
def test_inv_002_product_names_display(driver):
    inv.login_to_inventory(driver)
    names = driver.find_elements(*inv.ITEM_NAME)
    assert len(names) == inv.EXPECTED_ITEM_COUNT
    assert all(n.is_displayed() and n.text.strip() for n in names)


# INV-003 -- Long product name is displayed in full (not truncated).
def test_inv_003_long_product_name(driver):
    inv.login_to_inventory(driver)
    names = inv.names(driver)
    assert inv.LONGEST_NAME in names, "Longest product name not found intact"


# INV-004 -- Product descriptions are displayed.
def test_inv_004_product_descriptions_display(driver):
    inv.login_to_inventory(driver)
    descs = driver.find_elements(*inv.ITEM_DESC)
    assert len(descs) == inv.EXPECTED_ITEM_COUNT
    assert all(dsc.is_displayed() and dsc.text.strip() for dsc in descs)


# INV-005 -- Product prices are displayed.
def test_inv_005_product_prices_display(driver):
    inv.login_to_inventory(driver)
    price_els = driver.find_elements(*inv.ITEM_PRICE)
    assert len(price_els) == inv.EXPECTED_ITEM_COUNT
    assert all(p.text.startswith("$") for p in price_els)


# INV-006 -- Product images are displayed and actually load (no broken icons).
def test_inv_006_product_images_display(driver):
    inv.login_to_inventory(driver)
    imgs = driver.find_elements(*inv.ITEM_IMG)
    assert len(imgs) == inv.EXPECTED_ITEM_COUNT
    for img in imgs:
        assert img.get_attribute("src")
        # naturalWidth == 0 means a broken image.
        assert driver.execute_script("return arguments[0].naturalWidth", img) > 0


# INV-007 -- Add to Cart button is displayed.
def test_inv_007_add_button_display(driver):
    inv.login_to_inventory(driver)
    buttons = inv.add_buttons(driver)
    assert len(buttons) == inv.EXPECTED_ITEM_COUNT
    assert buttons[0].is_displayed()


# INV-008 -- Adding one product updates the cart badge to 1.
def test_inv_008_add_one_product(driver):
    inv.login_to_inventory(driver)
    inv.add_buttons(driver)[0].click()
    inv.wait(driver).until(EC.visibility_of_element_located(inv.CART_BADGE))
    assert inv.badge_count(driver) == 1


# INV-009 -- The same product can only be added once (button toggles to Remove).
def test_inv_009_multiple_clicks(driver):
    inv.login_to_inventory(driver)
    first = inv.add_buttons(driver)[0]
    first.click()
    inv.wait(driver).until(EC.visibility_of_element_located(inv.CART_BADGE))
    # Button toggled to Remove, so the product cannot be added a second time.
    assert inv.add_buttons(driver)[0].text == "Remove"
    assert inv.badge_count(driver) == 1


# INV-010 -- Remove button is displayed after adding a product.
def test_inv_010_remove_button_display(driver):
    inv.login_to_inventory(driver)
    inv.add_buttons(driver)[0].click()
    remove = inv.wait(driver).until(
        EC.visibility_of_element_located(inv.REMOVE_BUTTONS)
    )
    assert remove.is_displayed()
    assert remove.text == "Remove"


# INV-011 -- Removing a product restores the Add to Cart button.
def test_inv_011_remove_product(driver):
    inv.login_to_inventory(driver)
    inv.add_buttons(driver)[0].click()
    inv.wait(driver).until(EC.visibility_of_element_located(inv.REMOVE_BUTTONS))
    driver.find_element(*inv.REMOVE_BUTTONS).click()
    assert inv.add_buttons(driver)[0].text == "Add to cart"
    assert inv.badge_count(driver) == 0


# INV-012 -- Cart badge is displayed after adding a product.
def test_inv_012_badge_display(driver):
    inv.login_to_inventory(driver)
    inv.add_buttons(driver)[0].click()
    badge = inv.wait(driver).until(EC.visibility_of_element_located(inv.CART_BADGE))
    assert badge.is_displayed()


# INV-013 -- Cart badge shows the correct count for multiple products.
def test_inv_013_badge_count(driver):
    inv.login_to_inventory(driver)
    buttons = inv.add_buttons(driver)
    for i in range(3):
        inv.add_buttons(driver)[i].click()
    inv.wait(driver).until(EC.text_to_be_present_in_element(inv.CART_BADGE, "3"))
    assert inv.badge_count(driver) == 3


# INV-014 -- Cart badge disappears when the cart becomes empty.
def test_inv_014_badge_removal(driver):
    inv.login_to_inventory(driver)
    inv.add_buttons(driver)[0].click()
    inv.wait(driver).until(EC.visibility_of_element_located(inv.CART_BADGE))
    driver.find_element(*inv.REMOVE_BUTTONS).click()
    inv.wait(driver).until_not(EC.presence_of_element_located(inv.CART_BADGE))
    assert inv.badge_count(driver) == 0


# INV-015 -- Sorting control is displayed.
def test_inv_015_sort_control_display(driver):
    inv.login_to_inventory(driver)
    assert driver.find_element(*inv.SORT_SELECT).is_displayed()


# INV-016 -- Sort by Name (A to Z).
def test_inv_016_sort_name_az(driver):
    inv.login_to_inventory(driver)
    inv.select_sort(driver, "az")
    names = inv.names(driver)
    assert names == sorted(names)


# INV-017 -- Sort by Name (Z to A).
def test_inv_017_sort_name_za(driver):
    inv.login_to_inventory(driver)
    inv.select_sort(driver, "za")
    names = inv.names(driver)
    assert names == sorted(names, reverse=True)


# INV-018 -- Sort by Price (low to high).
def test_inv_018_sort_price_low_high(driver):
    inv.login_to_inventory(driver)
    inv.select_sort(driver, "lohi")
    price_list = inv.prices(driver)
    assert price_list == sorted(price_list)


# INV-019 -- Sort by Price (high to low).
def test_inv_019_sort_price_high_low(driver):
    inv.login_to_inventory(driver)
    inv.select_sort(driver, "hilo")
    price_list = inv.prices(driver)
    assert price_list == sorted(price_list, reverse=True)
