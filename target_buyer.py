import os
import time
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Navigate to the Target product page


# Loop until "Add to cart" button appears and is clickable
while True:
    try:
        print("Checking for 'Add to cart' button...")
        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Add to cart')]")))
        print("'Add to cart' button found and clickable!")
        add_to_cart_button.click()
        print("Clicked 'Add to cart' button.")

        # Send signal/event to target_buyer.py or another process

    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException) as e:
        print(f"'Add to cart' button not available yet. Retrying...")
        try:
            driver.refresh()
        except Exception as refresh_err:
            print("Refresh failed:", refresh_err)
        time.sleep(random.uniform(1, 3))  # Wait before retrying

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