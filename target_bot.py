import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Setup for Brave on Windows
options = Options()
options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

# Tell Selenium where to find chromedriver.exe
service = Service("./chromedriver.exe")

# Launch Brave browser via Selenium
driver = webdriver.Chrome(service=service, options=options)

# Go to a website
driver.get("https://www.google.com")
