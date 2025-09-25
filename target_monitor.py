import os
import time
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Kill any existing Brave processes
os.system("taskkill /F /IM brave.exe")

# Create options object from undetected_chromedriver, NOT normal Chrome
options = uc.ChromeOptions()

# Pass arguments correctly (these are for the browser, not URLs!)
options.add_argument("--user-data-dir=/tmp/brave_user_data")
options.add_argument("--profile-directory=Automation")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")

# Debugging: Print the options being passed
print("Launching Brave with the following options:")
print(options.arguments)

# Launch Brave via undetected_chromedriver
driver = uc.Chrome(options=options, version_main=135, browser_executable_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser')

# Optional: Maximize window
driver.maximize_window()

# Go to the Walmart product page
product_url = "https://www.target.com/p/pokemon-18-34-sleeping-plush-totodile/-/A-91959747#lnk=sametab"
print("Opening product page...")
driver.get(product_url)

# Wait for the page to load
wait = WebDriverWait(driver, 15)

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
        print(f"'Add to cart' button not available yet. Retrying... ({e})")
        time.sleep(2)  # Wait before retrying

# Wait for cart to update
time.sleep(3)

# Keep the browser open for observation
time.sleep(10)
driver.quit()
