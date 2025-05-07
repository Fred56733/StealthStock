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
product_url = "https://www.target.com/p/pok-233-mon-trading-card-game-scarlet-38-violet-8212-destined-rivals-elite-trainer-box/-/A-94300069"
print("Opening product page...")
driver.get(product_url)

# Wait for the page to load
wait = WebDriverWait(driver, 15)

# Loop until "Add to cart" button appears and is clickable
while True:
    print("🔁 Checking stock...")
    driver.refresh()
    time.sleep(2)

    try:
        button_xpath = "//button[@aria-label[contains(., 'Add to cart')]]"
        add_button = driver.find_element(By.XPATH, button_xpath)

        if add_button.is_enabled():
            print("✅ IN STOCK! Clicking 'Add to cart'...")

            try:
                driver.find_element(By.XPATH, button_xpath).click()
                print("✅ Clicked 'Add to Cart'!")
                break

            except ElementClickInterceptedException:
                print("⚠️ Click intercepted — possibly a popup. Retrying after short wait.")
                time.sleep(3)

        else:
            print("🟡 Button found but not enabled")

    except (NoSuchElementException, StaleElementReferenceException):
        print("❌ Button not found or stale, retrying...")

# Proceed to checkout
try:
    print("⏳ Waiting for cart-related button...")

    try:
        # Option 1: View Cart button
        cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View cart')]")))
        cart_button.click()
        print("✅ Clicked 'View Cart'!")

    except TimeoutException:
        try:
            # Option 2: Go to cart link
            cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Go to cart')]")))
            cart_button.click()
            print("✅ Clicked 'Go to Cart'!")

        except TimeoutException:
            try:
                # Option 3: Fallback - Cart icon in header
                print("⚠️ No cart modal — trying cart icon instead...")
                cart_icon = driver.find_element(By.ID, "cart-button-header")
                cart_icon.click()
                print("✅ Clicked cart icon in header!")

            except Exception as e:
                print("❌ Failed to click cart icon:", str(e))
                driver.quit()
                exit()

    # Continue to checkout once we're on cart page
    print("⏳ Waiting for 'Continue to checkout' button...")
    checkout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue to checkout')]")))
    checkout_button.click()
    print("✅ Clicked 'Proceed to Checkout'!")

except Exception as e:
    print("❌ Error during checkout:", str(e))

# Keep the browser open for observation
time.sleep(10)
driver.quit()
