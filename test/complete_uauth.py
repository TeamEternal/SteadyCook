# current file is OBSOLETE
# changed from automatic login to manual login

# file still may be used to test automated login on target site
# captcha may trigger which will cause the script to exit

import os
import time
from config import targets
from selenium import webdriver

# just launch a new instance of chrome everytime and log in
# site might detect multiple log-ins

print('**steadycook.py** [ INFO ] SteadyCook => Execution::StartingProgram...') 

def execute_auth(keys):
    dir = os.getcwd()

    print(f'**steadycook.py** [ STATUS ] SteadyCook => Loading chromedriver from {dir}/')
    driver = webdriver.Chrome(f'{dir}/chromedriver')
   
    print('**steadycook.py** [ \033[0;32mSUCCESS\033[0;m ] Chrome driver loaded successfully: Initializing browser...')
    # should not be logged in, new instance
    driver.get(keys['unauthorized_url'])

    print('**steadycook.py** [ INFO ] {ChromeStatus} => Automation of user-forms actively started')

    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[2]/main/div/form/div[1]/input').send_keys('userbot8') # username 
    # time.sleep(60)
    driver.find_element_by_xpath('/html/body/div[2]/main/div/form/div[2]/input').send_keys('12345678ASDF') # password
    # time.sleep(10)
    driver.find_element_by_xpath('/html/body/div[2]/main/div/form/div[4]/button').click() # click login
    print('**steadycook.py** [ \033[0;32mSUCCESS\033[0;m ] SteadyCook {ChromeStatus} => Static login for target domain completed')

    print('**steadycook.py** [ INFO ] SteadyCook => Starting search instance for Captcha...')
    captcha_true = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]')

    if str(captcha_true) != "" or None:
        print("\033[0;31m<SteadyCook => Exception::CaptchaDetected>\033[0;m")
        time.sleep(10)
        driver.quit()
    
    else:  # load booter
        driver.get(keys['authorized_url']) # try loading through get() method or clicking button link
        time.sleep(100)
        driver.quit()


# call main function, pass targets from config.py into program
execute_auth(targets)