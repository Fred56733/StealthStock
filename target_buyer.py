import os
import time
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Go to cart page
try:
    print("Navigating to cart page...")
    driver.get("https://www.target.com/cart")
    print("Cart page loaded.")
except Exception as e:
    print(f"Failed to load cart page: {e}")

# Maximize quantity if possible
try:
    print("Attempting to maximize item quantity...")
    select_el = wait.until(EC.presence_of_element_located((By.XPATH, "//select[@data-test='cartItem-qty']")))
    from selenium.webdriver.support.ui import Select
    select = Select(select_el)
    vals = [opt.get_attribute('value') for opt in select.options if opt.get_attribute('value')]
    max_val = max([int(v) for v in vals if v.isdigit()])
    select.select_by_value(str(max_val))
    print(f"Set item quantity to {max_val}.")
except (TimeoutException, NoSuchElementException) as e:
    print(f"Could not change item quantity: {e}")