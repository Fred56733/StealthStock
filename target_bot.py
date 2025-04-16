import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Kill any existing Brave processes
os.system("taskkill /F /IM brave.exe")

# Create options object from undetected_chromedriver, NOT normal Chrome
options = uc.ChromeOptions()

# Point to Brave binary (be sure this path is correct for your system)
options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

# Pass arguments correctly (these are for the browser, not URLs!)
options.add_argument("--user-data-dir=C:\\Users\\17726\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data")
options.add_argument("--profile-directory=Automation")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")

# Debugging: Print the options being passed
print("Launching Brave with the following options:")
print(options.arguments)

# Launch Brave via undetected_chromedriver
driver = uc.Chrome(options=options, version_main=135)

# Optional: Maximize window
driver.maximize_window()

# Go to the Walmart product page
product_url = "https://www.walmart.com/ip/Play-Day-Bubble-Stick-Blue-5-fl-oz-for-Child-Age-3/245888811"
print("Opening product page...")
driver.get(product_url)

# Wait for the page to load
wait = WebDriverWait(driver, 15)

# Try to click the "Add to Cart" button
try:
    # Step 1 "Add to Cart"
    add_button = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[@aria-label[contains(., 'Add to cart')]]"
    )))
    
    add_button.click()
    print("✅ Clicked 'Add to Cart'!")

    # Step 2 "Proceed to Checkout"
    view_cart_button = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[contains(text(), 'View cart')]"
    )))

    view_cart_button.click()
    print("✅ Clicked 'View Cart'!")

    continue_to_checkout_button = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//button[contains(text(), 'Continue to checkout')]"
    )))

    continue_to_checkout_button.click()
    print("✅ Clicked 'Proceed to Checkout'!")

except Exception as e:
    print("❌ Could not click 'Add to Cart'")
    print("Error:", str(e))

# Keep browser open for 10 seconds to observe the result
time.sleep(10)
driver.quit()
