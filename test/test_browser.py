import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 


chrome_options = Options()
# target port set to 9222, a function can be created to rand generate on the fly
# everytime the program is started up 
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

# change the chrome driver $PATH
driver = webdriver.Chrome(f'{os.getcwd()}/chromedriver', chrome_options=chrome_options)

print(driver.title)