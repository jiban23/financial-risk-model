"""Locators and helpers for the SauceDemo Login Module.

The test cases list https://www.saucedemo.com/v1/ as the URL; SauceDemo redirects
that to the current login page, so these locators target the served DOM.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_URL = "https://www.saucedemo.com/v1/"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"

USERNAME = (By.ID, "user-name")
PASSWORD = (By.ID, "password")
LOGIN_BUTTON = (By.ID, "login-button")
ERROR = (By.CSS_SELECTOR, "[data-test='error']")
ERROR_ICON = (By.CSS_SELECTOR, ".error_icon")

# Error strings SauceDemo returns (verified against the live site).
ERR_USERNAME_REQUIRED = "Epic sadface: Username is required"
ERR_PASSWORD_REQUIRED = "Epic sadface: Password is required"
ERR_NO_MATCH = "Epic sadface: Username and password do not match any user in this service"


def open_login(driver):
    driver.get(LOGIN_URL)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(USERNAME))


def enter_username(driver, text):
    field = driver.find_element(*USERNAME)
    field.send_keys(text)
    return field


def enter_password(driver, text):
    field = driver.find_element(*PASSWORD)
    field.send_keys(text)
    return field


def click_login(driver):
    driver.find_element(*LOGIN_BUTTON).click()


def error_text(driver):
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(ERROR)
    ).text


def error_icon_count(driver):
    return len(driver.find_elements(*ERROR_ICON))
