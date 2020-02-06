import os
from config import targets
from selenium import webdriver

# wasted like 2 hours, we dont need the token
# just launch a new instance of chrome everytime and log in
# site might detect multiple log-ins

def determine_auth(keys):

    dir = os.getcwd()
    driver = webdriver.Chrome(f'{dir}/chromedriver')
    
    # # get value from access token
    # with open(f'{dir}/token.txt', 'r') as f:
    #     access_token = str(f.readline())
    #     f.close()
    
    # # referencing the token as an int when it was converted to a string, stupid but who cares
    # if access_token == 0:
    #     driver.get(keys['not_authorized_url'])
    #     domain_status = driver.find_element_by_class_name("actions").text

    #     # its bad practice to nest if statements but ohh well
    #     if str(domain_status) == "Lost your password?":
    #         print("\033[0;31mThe client is not authorized\033[0;m")
    #         driver.quit()

    
    # should not be logged in, new instance
    driver.get(keys['authorized_url'])

    dashboard_status = driver.find_element_by_class_name('spaced').text
    print(dashboard_status)
        

    

    


# call main function, pass targets from config.py into program
determine_auth(targets)