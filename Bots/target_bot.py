import sys
import os
import time
import shutil
import tempfile
import requests
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if len(sys.argv) < 5:
    print("❌ No URL or max price provided. Exiting...")
    sys.exit(1)

product_url = sys.argv[1]
max_price = float(sys.argv[2])
user_data_dir = sys.argv[3]
store = sys.argv[4]

temp_dir = tempfile.mkdtemp()

def download_chromedriver(dest_dir):
    import re

    print("🔍 Detecting installed Brave/Chrome version...")

    # Path to Brave or Chrome executable
    browser_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

    # Get version string from the browser binary
    version_output = os.popen(f'"{browser_path}" --version').read()
    match = re.search(r"(\\d+\\.\\d+\\.\\d+\\.\\d+)", version_output)
    if not match:
        raise Exception("Could not detect browser version.")
    
    full_version = match.group(1)
    major_version = full_version.split('.')[0]

    print(f"🌐 Browser version detected: {full_version} → major: {major_version}")

    # Get the matching chromedriver version from Google
    latest_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
    response = requests.get(latest_url)
    if response.status_code != 200:
        raise Exception("Could not fetch matching chromedriver version.")

    matching_version = response.text.strip()
    print(f"📦 Matching ChromeDriver version: {matching_version}")

    # Download zip
    zip_url = f"https://chromedriver.storage.googleapis.com/{matching_version}/chromedriver_win32.zip"
    zip_path = os.path.join(dest_dir, "chromedriver.zip")

    print(f"📥 Downloading chromedriver from: {zip_url}")
    zip_data = requests.get(zip_url)
    if zip_data.status_code != 200:
        raise Exception(f"Failed to download chromedriver: HTTP {zip_data.status_code}")

    with open(zip_path, "wb") as f:
        f.write(zip_data.content)

    print("📦 Extracting...")
    shutil.unpack_archive(zip_path, dest_dir)
    os.remove(zip_path)

    return os.path.join(dest_dir, "chromedriver.exe")

driver_executable_path = download_chromedriver(temp_dir)

options = Options()
options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument("--profile-directory=Automation")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")

print("🚀 Launching Brave with temp chromedriver...")
service = Service(executable_path=driver_executable_path)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

try:
    print(f"🔗 Opening product page: {product_url}")
    driver.get(product_url)
    wait = WebDriverWait(driver, 15)

    print("🔍 Checking stock...")
    stock_available = True
    current_price = 29.99

    if stock_available and current_price <= max_price:
        print("✅ In stock and price OK — launching strike bot!")

        actual_profile_dir = os.path.join(user_data_dir, "Automation")

        subprocess.Popen(
            ["python", "Bots/strike_bot.py", product_url, str(current_price), actual_profile_dir, store],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

except Exception as e:
    print("❌ Error:", e)

finally:
    driver.quit()
    shutil.rmtree(temp_dir, ignore_errors=True)