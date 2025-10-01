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
    brave_data_path = r"C:\Users\17726\AppData\Local\BraveSoftware\Brave-Browser\User Data"
    
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
    print(f"💰 Max price set to: ${product['max_price']}")
    driver = launch_brave(product.get("profile", "Automation"))
    wait = WebDriverWait(driver, 15)

    print("🌐 Opening product page...")
    driver.get(product["url"])

    # Checks items stock (on loop)
    while True:
        print("🔁 Checking stock...")
        driver.refresh()
        time.sleep(2)

        # Check price first
        try:
            price_element = driver.find_element(By.XPATH, "//span[@itemprop='price']")
            price_text = price_element.text.replace('$', '').replace(',', '')
            current_price = float(price_text)
            print(f"💵 Current price: ${current_price}")
            
            if current_price > product['max_price']:
                print(f"❌ Price ${current_price} exceeds max price ${product['max_price']} - skipping")
                time.sleep(5)  # Wait before checking again
                continue
            else:
                print(f"✅ Price ${current_price} is within budget!")
                
        except (NoSuchElementException, ValueError) as e:
            print(f"⚠️ Could not get price: {e}")
            # Continue anyway if price can't be found
            pass

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

    # Immediately go to cart after adding item
    try:
        print("🛒 Clicking cart button in header...")
        time.sleep(2)  # Brief wait for cart to update
        cart_icon = wait.until(EC.element_to_be_clickable((By.ID, "cart-button-header")))
        cart_icon.click()
        print("🛒 Navigated to cart!")

        # Maximize quantity if specified
        if product.get('max_quantity', 1) > 1:
            try:
                print(f"🔢 Attempting to set quantity to {product['max_quantity']}...")
                time.sleep(3)  # Wait longer for cart page to fully load
                
                # Find the current quantity with a more reliable selector
                current_qty_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-testid='quantity-label']")))
                current_qty = int(current_qty_element.text.strip())
                print(f"📊 Current quantity: {current_qty}")
                
                # Calculate clicks needed
                target_qty = product['max_quantity']
                clicks_needed = target_qty - current_qty
                
                if clicks_needed > 0:
                    print(f"🔄 Need to click plus button {clicks_needed} times...")
                    
                    # More reliable plus button selector
                    plus_button = driver.find_element(By.XPATH, "//i[@data-testid='quantity-stepper-inc-icon']/..")
                    
                    for i in range(clicks_needed):
                        try:
                            print(f"🔄 Clicking plus button (attempt {i+1}/{clicks_needed})...")
                            plus_button.click()
                            time.sleep(0.5)  # Slightly longer delay
                            
                            # Re-find button in case DOM updates
                            plus_button = driver.find_element(By.XPATH, "//i[@data-testid='quantity-stepper-inc-icon']/..")
                            
                            # Check if button becomes disabled
                            if plus_button.get_attribute("aria-disabled") == "true":
                                print("⚠️ Reached maximum quantity limit!")
                                break
                                
                        except (ElementClickInterceptedException, NoSuchElementException) as e:
                            print(f"⚠️ Could not increase quantity further: {e}")
                            break
                    
                    print(f"✅ Quantity adjustment complete!")
                else:
                    print(f"✅ Quantity already at desired level: {current_qty}")
                
            except (TimeoutException, NoSuchElementException, ValueError) as e:
                print(f"⚠️ Could not modify quantity: {e}")
                print("🔄 Continuing to checkout anyway...")

        print("⏳ Waiting for 'Continue to checkout' button...")
        checkout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue to checkout')]")))
        checkout_button.click()
        print("✅ Proceeded to checkout!")

        # Wait for checkout page to load and find "Place order" button
        print("⏳ Waiting for checkout page to load...")
        time.sleep(3)  # Give checkout page time to load
        
        try:
            print("🔍 Looking for 'Place order' button...")
            place_order_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='place-order-button']")))
            
            # Get the total price from the button text
            button_text = place_order_button.text
            print(f"💳 Found order button: {button_text}")
            
            place_order_button.click()
            print("🎉 ORDER PLACED SUCCESSFULLY! 🎉")
            
        except TimeoutException:
            print("❌ Could not find 'Place order' button - checkout may require manual completion")
            # Try alternative selectors
            try:
                place_order_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Place order')]")))
                place_order_button.click()
                print("🎉 ORDER PLACED SUCCESSFULLY (alternative selector)! 🎉")
            except TimeoutException:
                print("❌ Manual checkout completion required")

    except Exception as e:
        print("❌ Error during checkout:", e)

    # Keep browser open longer to see results
    print("⏳ Keeping browser open for 300 seconds to verify order...")
    time.sleep(300)
    driver.quit()

if __name__ == "__main__":
    # Example product - replace with your actual product
    product = {
        "name": "HengDidi Durable Car Wheel Hub Brush",
        "url": "https://www.walmart.com/ip/HengDidi-Durable-Car-Wheel-Hub-Brush-Dual-Color-Bristles-for-Tire-Rim-Deep-Cleaning-with-Compact-Anti-Slip-Handle/16642907658?classType=VARIANT&athbdg=L1400",
        "profile": "Automation",
        "max_price": 3.52,
        "max_quantity": 1
    }
    
    run(product)
