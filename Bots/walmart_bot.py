import sys
import os
import time
import random
import tempfile
import shutil
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get the product URL from the command-line arguments
if len(sys.argv) < 5:
    print("❌ No URL or max price provided. Exiting...")
    sys.exit(1)
product_url = sys.argv[1]
max_price = float(sys.argv[2])
user_data_dir = sys.argv[3]
store = sys.argv[4]

# Create a unique temporary directory for this bot instance
temp_dir = tempfile.mkdtemp()
driver_executable_path = os.path.join(temp_dir, "chromedriver.exe")

# Initialize the browser
options = uc.ChromeOptions()
options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
options.add_argument("--user-data-dir=C:\\Users\\17726\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data")
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Automation2")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")

# Debugging: Print the options being passed
print("Launching Brave with the following options:")
print(options.arguments)

try:
    # Launch the browser with the isolated driver
    driver = uc.Chrome(
        options=options,
        driver_executable_path=driver_executable_path,
        version_main=135  # Match your local Chrome major version
    )

    driver.maximize_window()

# Navigate to the Walmart product page
print(f"Opening product page: {product_url}")
driver.get(product_url)

# Wait for the page to load
wait = WebDriverWait(driver, 15)

# Function to extract the price
def get_price():
    try:
        price_element = driver.find_element(By.XPATH, "//span[@itemprop='price']")
        price_text = price_element.text.replace("$", "").replace(",", "").replace("Now", "").strip()  # Clean the text
        price = float(price_text)  # Convert cleaned text to a float        
        print(f"💲 Current price: ${price}")
        return price
    except NoSuchElementException:
        print("❌ Price element not found. Retrying...")
        return None
    except ValueError:
        print("❌ Error converting price to float. Retrying...")
        return None

# Check the price
while True:
    print("🔁 Checking price...")
    driver.refresh()
    time.sleep(random.uniform(2, 5)) # Random delay between 2 and 5 seconds

    current_price = get_price()
    if current_price is not None:
        if current_price <= max_price:
            print(f"✅ Price is within range: ${current_price} (<= ${max_price})")
            break
        else:
            print(f"🟡 Price is too high: ${current_price} (> ${max_price})")
    else:
        print("❌ Unable to retrieve price. Retrying...")

# Check stock and add to cart
while True:
    print("🔁 Checking stock...")
    driver.refresh()
    time.sleep(random.uniform(2, 5))  # Random delay between 2 and 5 seconds

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
