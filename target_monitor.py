import os, time, argparse, random, tempfile, atexit, shutil
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Parse command-line arguments for link
parser = argparse.ArgumentParser()
parser.add_argument("--product-url", help="Product URL to monitor (overrides products.json)")
args = parser.parse_args()
product_url = args.product_url or os.environ.get("PRODUCT_URL")

# Kill any existing Brave processes
os.system("taskkill /F /IM brave.exe")

# Create options object from undetected_chromedriver, NOT normal Chrome
options = uc.ChromeOptions()

# Create an isolated temp profile for this monitor process (avoids profile lock)
tmp_profile = tempfile.mkdtemp(prefix="brave_mon_")
atexit.register(lambda: shutil.rmtree(tmp_profile, ignore_errors=True))
options.add_argument(f"--user-data-dir={tmp_profile}")

# Pass arguments correctly (these are for the browser, not URLs!)
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

# Ensure we have a product URL and open it
if not product_url:
    print("No product URL provided. Use --product-url or set PRODUCT_URL env var.")
    driver.quit()
    raise SystemExit(1)

print(f"Opening product URL: {product_url}")
driver.get(product_url)
time.sleep(2)

# Wait for the page to load
wait = WebDriverWait(driver, random.uniform(5, 10))

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

# Keep the browser open for observation
time.sleep(10)
driver.quit()
