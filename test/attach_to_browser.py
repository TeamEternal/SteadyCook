import os
import time
from selenium import webdriver

path = os.getcwd()

driver = webdriver.Chrome(f'{path}/chromedriver')

url = driver.command_executor._url
session_id = driver.session_id

driver = webdriver.Remote(command_executor=url, desired_capabilities={})
driver.session_id = session_id

driver.get('http://www.google.com') # target website is not listed for privacy reasons

time.sleep(10)