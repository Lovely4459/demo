from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

# If chromedriver.exe is in the same directory as the script
service = Service(executable_path="./chromedriver.exe")
driver = webdriver.Chrome(service=service) 

driver.get("https://google.com")

time.sleep(60)

driver.quit()
