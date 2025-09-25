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

