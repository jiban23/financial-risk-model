"""Navigation menu test suite (NAV-001 .. NAV-010), cross-browser.

Each case runs across every browser in ``--browsers`` (default: chrome,
firefox, edge, opera) via the parametrized ``driver`` fixture in this folder's
conftest.py; unavailable browsers are skipped. Every test logs in first, since
the burger menu is only reachable from the inventory page.
"""
import pytest
from selenium.webdriver.support import expected_conditions as EC

import navigation_page as nav


# NAV-001 -- Menu button is displayed.
def test_nav_001_menu_button_display(driver):
    nav.login_to_inventory(driver)
    assert driver.find_element(*nav.MENU_BUTTON).is_displayed()


# NAV-002 -- Navigation menu is displayed after clicking the Menu button.
def test_nav_002_open_menu(driver):
    nav.login_to_inventory(driver)
    nav.open_menu(driver)
    assert nav.menu_is_open(driver)
    assert driver.find_element(*nav.ALL_ITEMS_LINK).is_displayed()


# NAV-003 -- All Items option is displayed in the open menu.
def test_nav_003_all_items_display(driver):
    nav.login_to_inventory(driver)
    nav.open_menu(driver)
    all_items = driver.find_element(*nav.ALL_ITEMS_LINK)
    assert all_items.is_displayed()
    assert all_items.text == "All Items"


# NAV-004 -- Selecting All Items shows the Inventory Module.
def test_nav_004_all_items_shows_inventory(driver):
    nav.login_to_inventory(driver)
    nav.open_menu(driver)
    nav.click_menu_link(driver, nav.ALL_ITEMS_LINK)
    nav.wait(driver).until(EC.url_contains("inventory.html"))
    assert driver.find_element(*nav.INVENTORY_CONTAINER).is_displayed()


# NAV-005 -- About option is displayed in the open menu.
def test_nav_005_about_display(driver):
    nav.login_to_inventory(driver)
    nav.open_menu(driver)
    about = driver.find_element(*nav.ABOUT_LINK)
    assert about.is_displayed()
    assert about.text == "About"


# NAV-006 -- Selecting About opens the Sauce Labs website.
def test_nav_006_about_opens_website(driver):
    nav.login_to_inventory(driver)
    nav.open_menu(driver)
    # The About link points to the Sauce Labs marketing site.
    assert nav.ABOUT_URL in driver.find_element(*nav.ABOUT_LINK).get_attribute("href")
    nav.click_menu_link(driver, nav.ABOUT_LINK)
    nav.wait(driver).until(EC.url_contains(nav.ABOUT_URL))
    assert nav.ABOUT_URL in driver.current_url


# NAV-007 -- Reset App State option is displayed in the open menu.
def test_nav_007_reset_display(driver):
    nav.login_to_inventory(driver)
    nav.open_menu(driver)
    reset = driver.find_element(*nav.RESET_LINK)
    assert reset.is_displayed()
    assert reset.text == "Reset App State"


# NAV-008 -- Reset App State clears the cart badge.
def test_nav_008_reset_app_state(driver):
    nav.login_to_inventory(driver)
    nav.add_first_product(driver)
    assert nav.badge_count(driver) == 1

    nav.open_menu(driver)
    nav.click_menu_link(driver, nav.RESET_LINK)
    nav.wait(driver).until_not(EC.presence_of_element_located(nav.CART_BADGE))

    assert nav.badge_count(driver) == 0


# NAV-008 (cont.) -- Reset should also un-mark added products (revert Remove
# back to Add to cart). This is a KNOWN SauceDemo defect: Reset App State
# clears the cart badge but leaves the inventory buttons on "Remove" until the
# page is reloaded. Marked xfail so the suite stays green while still tracking
# the bug -- it will surface as XPASS if SauceDemo ever fixes it.
@pytest.mark.xfail(reason="SauceDemo bug: Reset App State does not revert "
                          "inventory button labels until page reload",
                   strict=False)
def test_nav_008b_reset_unmarks_products(driver):
    nav.login_to_inventory(driver)
    nav.add_first_product(driver)
    nav.open_menu(driver)
    nav.click_menu_link(driver, nav.RESET_LINK)
    nav.wait(driver).until_not(EC.presence_of_element_located(nav.CART_BADGE))

    assert not driver.find_elements(*nav.REMOVE_BUTTONS)


# NAV-009 -- Logout option is displayed in the open menu.
def test_nav_009_logout_display(driver):
    nav.login_to_inventory(driver)
    nav.open_menu(driver)
    logout = driver.find_element(*nav.LOGOUT_LINK)
    assert logout.is_displayed()
    assert logout.text == "Logout"


# NAV-010 -- Logout returns the user to the Login Module.
def test_nav_010_logout_user(driver):
    nav.login_to_inventory(driver)
    nav.open_menu(driver)
    nav.click_menu_link(driver, nav.LOGOUT_LINK)
    nav.wait(driver).until(EC.visibility_of_element_located(nav.LOGIN_BUTTON))
    assert driver.find_element(*nav.LOGIN_BUTTON).is_displayed()
    assert driver.find_element(*nav.USERNAME).is_displayed()
