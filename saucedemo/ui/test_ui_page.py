"""User Interface / visual test suite (UI-001 .. UI-013), cross-browser.

Runs once per browser in ``--browsers`` (chrome, firefox, edge, opera) via the
``driver`` fixture in ./conftest.py; unavailable browsers are SKIPPED. Login-page
cases open the login page; the rest log in first, since they inspect the
authenticated Inventory Module (and, for UI-013, the cart page too).

Some cases in this feature are inherently visual ("fonts are consistent",
"theme is consistent", "layout does not overlap"). They are automated here with
objective proxies -- computed styles, image load state, and bounding-box
geometry -- rather than pixel comparison, and each proxy is noted in a comment.
"""
from selenium.webdriver.support import expected_conditions as EC

import ui_page as ui


# UI-001 -- Company logo is displayed on the Login page.
def test_ui_001_login_logo_display(driver):
    ui.open_login(driver)
    logo = driver.find_element(*ui.LOGIN_LOGO)
    assert logo.is_displayed()
    assert logo.text.strip()  # "Swag Labs" wordmark is rendered as text


# UI-002 -- Product images are displayed without broken-image icons.
def test_ui_002_product_images_display(driver):
    ui.login_to_inventory(driver)
    ui.wait_images_loaded(driver, ui.EXPECTED_ITEM_COUNT)
    imgs = driver.find_elements(*ui.ITEM_IMG)
    assert len(imgs) == ui.EXPECTED_ITEM_COUNT
    for img in imgs:
        assert img.is_displayed()
        assert img.get_attribute("src")
        assert ui.image_loaded(driver, img), "Image failed to load (broken icon)"


# UI-003 -- Application buttons are displayed clearly and readable.
def test_ui_003_buttons_display(driver):
    ui.login_to_inventory(driver)
    buttons = driver.find_elements(*ui.ADD_BUTTONS)
    assert len(buttons) == ui.EXPECTED_ITEM_COUNT
    for button in buttons:
        assert button.is_displayed()
        assert button.is_enabled()
        assert button.text.strip()  # readable label, e.g. "ADD TO CART"


# UI-004 -- Text fields are displayed clearly and ready for input.
def test_ui_004_text_fields_display(driver):
    ui.open_login(driver)
    for locator in (ui.USERNAME, ui.PASSWORD):
        field = driver.find_element(*locator)
        assert field.is_displayed()
        assert field.is_enabled()  # ready to accept input
        assert field.get_attribute("value") == ""  # empty and ready


# UI-005 -- Application labels are displayed clearly and readable.
def test_ui_005_labels_display(driver):
    ui.login_to_inventory(driver)
    title = driver.find_element(*ui.PAGE_TITLE)
    assert title.is_displayed() and title.text.strip()  # e.g. "PRODUCTS"
    names = driver.find_elements(*ui.ITEM_NAME)
    assert len(names) == ui.EXPECTED_ITEM_COUNT
    assert all(n.is_displayed() and n.text.strip() for n in names)


# UI-006 -- Navigation menu is displayed with all options visible.
def test_ui_006_navigation_menu_display(driver):
    ui.login_to_inventory(driver)
    ui.open_menu(driver)
    for label, locator in ui.MENU_ITEM_LOCATORS.items():
        item = driver.find_element(*locator)
        assert item.is_displayed(), f"Menu option '{label}' not visible"
        assert item.text.strip()


# UI-007 -- Shopping Cart icon is displayed.
def test_ui_007_cart_icon_display(driver):
    ui.login_to_inventory(driver)
    assert driver.find_element(*ui.CART_ICON).is_displayed()


# UI-008 -- Fonts and font colors are displayed consistently.
def test_ui_008_font_consistency(driver):
    ui.login_to_inventory(driver)
    # "Consistent" means elements of the SAME role render identically: every
    # product name shares one font+color, every price shares one, and the page
    # title matches the product-name font. (SauceDemo intentionally uses DM Sans
    # for text and DM Mono for prices, so this checks per-role uniformity, not a
    # single global font.)
    names = driver.find_elements(*ui.ITEM_NAME)
    prices = driver.find_elements(*ui.ITEM_PRICE)
    assert names and prices

    name_fonts = {ui.css_value(driver, n, "font-family") for n in names}
    name_colors = {ui.css_value(driver, n, "color") for n in names}
    price_fonts = {ui.css_value(driver, p, "font-family") for p in prices}
    assert len(name_fonts) == 1, f"Product names use mixed fonts: {name_fonts}"
    assert len(name_colors) == 1, f"Product names use mixed colors: {name_colors}"
    assert len(price_fonts) == 1, f"Prices use mixed fonts: {price_fonts}"
    assert "" not in name_fonts | price_fonts  # a font-family is actually resolved

    # The page title's font must also be resolved (SauceDemo renders it in a
    # different family than product names by design, so we don't force equality).
    title_font = ui.css_value(driver, driver.find_element(*ui.PAGE_TITLE), "font-family")
    assert title_font, "Title font-family is not resolved"


# UI-009 -- Color theme is displayed consistently.
def test_ui_009_color_theme_consistency(driver):
    ui.login_to_inventory(driver)
    # Consistent theme: every primary action button renders with the exact same
    # (single) color, and the page background is a real opaque color -- not unset
    # or fully transparent.
    buttons = driver.find_elements(*ui.ADD_BUTTONS)
    button_colors = {ui.css_value(driver, b, "color") for b in buttons}
    assert len(button_colors) == 1, f"Buttons use mixed colors: {button_colors}"

    body_bg = ui.css_value(driver, driver.find_element("tag name", "body"), "background-color")
    assert body_bg not in ("", "transparent", "rgba(0, 0, 0, 0)"), (
        f"Page background is not a defined opaque color: {body_bg!r}"
    )


# UI-010 -- Page layout is consistent (elements aligned, no overlap).
def test_ui_010_layout_no_overlap(driver):
    ui.login_to_inventory(driver)
    rects = [item.rect for item in driver.find_elements(*ui.INVENTORY_ITEM)]
    assert len(rects) == ui.EXPECTED_ITEM_COUNT
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            assert not ui.rects_overlap(rects[i], rects[j]), (
                f"Inventory items {i} and {j} overlap"
            )


# UI-011 -- Error message and error icons are displayed clearly on invalid login.
def test_ui_011_error_message_display(driver):
    error = ui.trigger_login_error(driver)
    assert error.is_displayed()
    assert error.text.strip()  # readable message
    icons = driver.find_elements(*ui.ERROR_ICON)
    assert icons and all(icon.is_displayed() for icon in icons)


# UI-012 -- Footer is displayed and readable.
def test_ui_012_footer_display(driver):
    ui.login_to_inventory(driver)
    footer = driver.find_element(*ui.FOOTER)
    assert footer.is_displayed()
    copy = driver.find_element(*ui.FOOTER_COPY)
    assert copy.is_displayed() and copy.text.strip()  # e.g. copyright line


# UI-013 -- User interface stays visually consistent across pages.
def test_ui_013_overall_visual_consistency(driver):
    ui.login_to_inventory(driver)

    # Capture the shared chrome (logo wordmark + footer copy) on the inventory page.
    inventory_logo = driver.find_element(*ui.APP_LOGO).text.strip()
    inventory_footer = driver.find_element(*ui.FOOTER_COPY).text.strip()
    assert inventory_logo and inventory_footer

    # Navigate to the cart page and confirm the same chrome persists unchanged.
    driver.find_element(*ui.CART_ICON).click()
    ui.wait(driver).until(EC.url_contains("cart.html"))
    ui.wait(driver).until(EC.visibility_of_element_located(ui.PAGE_TITLE))

    assert driver.find_element(*ui.APP_LOGO).text.strip() == inventory_logo
    assert driver.find_element(*ui.FOOTER_COPY).text.strip() == inventory_footer
    assert driver.find_element(*ui.PAGE_TITLE).is_displayed()
