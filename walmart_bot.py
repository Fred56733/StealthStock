import os
import time
import sys
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def launch_brave(profile_name="Automation"):
    """Launch Brave browser with undetected chromedriver"""
    # Kill any existing Brave processes
    os.system("taskkill /F /IM brave.exe")
    
    options = uc.ChromeOptions()
    brave_data_path = r"C:\temp\brave_automation"
    
    options.add_argument(f"--user-data-dir={brave_data_path}")
    options.add_argument(f"--profile-directory={profile_name}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.headless = False
    
    print("🚀 Launching Brave with options:", options.arguments)
    
    driver = uc.Chrome(
        options=options,
        version_main=140, 
        browser_executable_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    )
    driver.maximize_window()
    return driver

def run(product):
    print(f"\n🚀 Starting Walmart bot for: {product['name']}")
    driver = launch_brave(product.get("profile", "Automation"))
    wait = WebDriverWait(driver, 15)

    print("🌐 Opening product page...")
    driver.get(product["url"])

    # Checks items stock (on loop)
    while True:
        print("🔁 Checking stock...")
        driver.refresh()
        time.sleep(2)

        # Look for add to cart
        try:
            button_xpath = "//button[@aria-label[contains(., 'Add to cart')]]"
            add_button = driver.find_element(By.XPATH, button_xpath)

            # When in stock add to cart 
            if add_button.is_enabled():
                print("✅ IN STOCK! Clicking 'Add to cart'...")
                try:
                    add_button.click()
                    print("✅ Added to cart!")
                    break
                except ElementClickInterceptedException:
                    print("⚠️ Click intercepted — retrying...")
                    time.sleep(3)
            else:
                print("🟡 Button present but not enabled")

        except (NoSuchElementException, StaleElementReferenceException):
            print("❌ Button not found or stale — retrying")

    try:
        print("⏳ Waiting for cart button...")

        try:
            cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View cart')]")))
            cart_button.click()
            print("🛒 Clicked 'View Cart'")
        except TimeoutException:
            try:
                cart_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Go to cart')]")))
                cart_button.click()
                print("🛒 Clicked 'Go to Cart'")
            except TimeoutException:
                try:
                    print("⚠️ Trying cart icon fallback...")
                    cart_icon = driver.find_element(By.ID, "cart-button-header")
                    cart_icon.click()
                    print("🛒 Clicked cart icon")
                except Exception as e:
                    print("❌ Failed to access cart:", e)
                    driver.quit()
                    return

        print("⏳ Waiting for 'Continue to checkout' button...")
        checkout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue to checkout')]")))
        checkout_button.click()
        print("✅ Proceeded to checkout!")

    except Exception as e:
        print("❌ Error during checkout:", e)

    time.sleep(10)
    driver.quit()

if __name__ == "__main__":
    # Example product - replace with your actual product
    product = {
        "name": "Mega Evo Lucario ETB",
        "url": "https://www.walmart.com/ip/17576818418",
        "profile": "Automation"
    }
    
    run(product)
