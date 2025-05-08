import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if len(sys.argv) < 5:
    print("❌ Missing arguments. Exiting...")
    sys.exit(1)

product_url = sys.argv[1]
price = float(sys.argv[2])
user_data_dir = sys.argv[3]
store = sys.argv[4]

# Initialize the browser
options = uc.ChromeOptions()
options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Default")  # Use the default profile
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")

# Launch the browser
driver = uc.Chrome(options=options)
driver.get(product_url)

try:
    # Add to cart
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-test='addToCartButton']"))
    )
    add_to_cart_button.click()
    print("✅ Added to cart.")

    # Proceed to checkout
    checkout_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Proceed to checkout')]"))
    )
    checkout_button.click()
    print("✅ Proceeding to checkout.")
except Exception as e:
    print(f"❌ Error during checkout: {e}")
finally:
    driver.quit()