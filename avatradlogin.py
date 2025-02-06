import logging
import time
import json
import requests
import alerts
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

#  Setup Logging
logging.basicConfig(
    filename="test_log.log",  
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

#  Get ChromeDriver Path from Docker ENV
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "/usr/bin/chromedriver")

#  Setup Chrome WebDriver options for Docker
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/chromium"  # Set Chromium path from Docker
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Anti-detection
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")

#  Function to send alerts
def send_alerts(error_message):
    logging.error(f"{error_message}")  
    alerts.send_slack_alert(error_message)  

#  Login automation script
def login_script():
    try:
        # Use ChromeDriver from Docker image
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        #  Open Website
        logging.info("Opening website...")
        driver.get("https://www.avatrade.com/")
        time.sleep(2)

        #  Locate and Click Login Button
        try:
            time.sleep(5)
            locate_login_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='wrapper-login']//span[@class='link-btn']"))
            )
            locate_login_button.click()
            logging.info(" Clicked on login button.")
        except TimeoutException:
            send_alerts(" Login button not found")
            driver.quit()
            return {'statuscode': 500, 'message': 'Login button not found'}

        #  Enter Username
        try:
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='input-email']"))
            )
            username.click()
            username.send_keys("test@noc-test.com")
            logging.info(" Entered username.")
            time.sleep(2)
        except TimeoutException:
            send_alerts(" Username field not found")
            driver.quit()
            return {'statuscode': 500, 'message': 'Username field not found'}

        #  Enter Password
        try:
            password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password.click()
            password.send_keys("T3Rau8S5dKB4@2!")
            logging.info(" Entered password.")
            time.sleep(2)
        except TimeoutException:
            send_alerts(" Password field not found")
            driver.quit()
            return {'statuscode': 500, 'message': 'Password field not found'}

        #  Click Login Button
        try:
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn_ga_real_main menu_cfd")) #d
            )
            login_button.click()
            logging.info(" Clicked on Login submit button.")
            time.sleep(5)
        except TimeoutException:
            send_alerts(" Login submission button not found")
            driver.quit()
            return {'statuscode': 500, 'message': 'Login submission button not found'}

        #  Check if login was successful
        try:
            check_if_login = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "mainWrapper"))
            )
            logging.info(" Login Successful. Found mainWrapper.")
        except TimeoutException:
            send_alerts(" Login failed")
            driver.quit()
            return {'statuscode': 500, 'message': 'Login failed'}

        #  Close browser after success
        time.sleep(2)
        driver.quit()
        logging.info(" Test Completed Successfully.")
        return {'statuscode': 200, 'message': 'Login successful'}

    except Exception as e:
        send_alerts(f" Unexpected error: {e}")
        return {'statuscode': 500, 'message': 'Unexpected error occurred'}

#  Run the function
response = login_script()
print(response)
