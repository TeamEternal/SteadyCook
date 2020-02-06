import os
import sys
import time
import subprocess
from datetime import datetime
from config import call_config_instance
from pynput.keyboard import Key, Listener
from getpass import getpass as getpassword

# this file is designated to be used as a central handler for base installation and setup
# steps for full build, 1. get chrome path, 2. install pip depenencies, 3. ask for automatic login, 4. autoload drivers to $CWD
# need to also run config.py to generate setting.ini configuration file last
'''
target features:
1.) Ability to handle and use a custom google chrome profile 
2.) Automated installation of pip dependencies
3.) Ability to setup automatic login
4.) Autoload drivers by extracting from $CWD/driver_src
'''

print('''-- INFO --
\033[0;33mThis is the first time that SteadyCook has been setup on the current system
\'setup.py\' will automatically set configuration parameters and other variables
that might be needed to run steadycook.py successfully\033[0;m

It is recommended that you emulate the current virtual environment in which
steadycook was built off of. You can do this by executing the following command:
\033[0;32m\'virtualenv Project_SteadyCook --python=python3.6 --system-site-packages\'\033[0;m
''')

KEY_STATUS = ''
POS_VAL = ['y', 'Y', 'yes', 'YES']
# BASE_DIRECTORY = f'{os.getcwd()}/Project_SteadyCook'
BASE_DIRECTORY = os.getcwd()


def key_return_status(key):
    global KEY_STATUS
    target_keys = [Key.shift, Key.shift_r]

    if key in target_keys:
        KEY_STATUS = 'clicked'

        return False

def key_listener():
    with Listener(on_press=key_return_status, on_release=None) as listener:
        listener.join()

# automate stressthem login
def get_automation_instance():
    global POS_VAL
    global BASE_DIRECTORY

    print('\033[0;32mINFO\033[0;m: This part will setup and configure the automatic',
        'login options for SteadyCook -> users can define wether or not SteadyCook will',
        'automatically login for the client at program execution (POST startup)', sep='\n')
    automate = str(input('\nSetup and enable automatic login functionality (default=no): '))

    if automate in POS_VAL:
        print('Generating target \033[0;32m\'clientauth\'\033[0;m file descriptor...')
        try:
            with open(f'{BASE_DIRECTORY}/clientauth.txt', 'w') as c:
                c.write('') # leave blank for user data
        
        except Exception as error:
            print('FATAL: Failed to generate a user file successfully! In order to automate logins follow:',
            f'Create target file by: \033[0;32m\'touch {BASE_DIRECTORY}clientauth.txt\'\033[0;m ', 
            'Write $USERNAME:$PASSWORD in the format as \'user:pass\'', sep='\n')
        
            sys.exit(1)

        else:
            # get user data
            username = str(input('Username: '))
            password = getpassword('Password: ')

            with open(f'{BASE_DIRECTORY}/clientauth.txt', 'w') as client:
                fmt = f'{username}:{password}'
                client.write(fmt.strip('\n'))
            
            print('Successfully setup and generated \'clientauth.txt\' for user-stored automatic login information')
    
    else:
        print('\033[0;33mWARNING\033[0;m: If you want to enable automatic login functionality execute the following',
            '\033[0;32m\'echo \"YOUR_USERNAME:YOUR_PASSWORD\" > clientauth.txt\'\033[0;m',
            'Then you will need to set \033[0;33mautomate_stressthem_login\033[0;m inside of \'settings.ini\' to \'yes\' ',
            '\n[ \033[0;32mOK\033[0;m ] Skipping generation of automatic login \'clientauth\' file', sep='\n')

        
def generate_exec(path): # '/path/Project_SteadyCook/exec.sh'
    global BASE_DIRECTORY

    print(f'[ INFO ] Creating \'{BASE_DIRECTORY}/exec.sh\' for google chrome debugging browser')
    subprocess.call(f'touch {BASE_DIRECTORY}/exec.sh ; chmod +x exec.sh', shell=True)



    define_port = "TARGET_PORT=$(awk -F \"=\" \'/target_port/ {print $2}\' settings.ini | sed -e \'s/^[[:space:]]*//\')\n"
    define_string = f'exec_string=\"Google\ Chrome --remote-debugging-port=$TARGET_PORT --user-data-dir={path}\"\n'
    eval_string = 'eval $exec_string'

    # cant use formated string literals due to limitations of using awk to get .ini configuration data
    load_file = define_port + define_string + eval_string

    print(f'[ STATUS ] SteadyCook => Writing {load_file} into \033[0;32m\'exec.sh\'\033[0;m')
    with open(f'{BASE_DIRECTORY}/exec.sh', 'w') as e_file:
        e_file.write(str(load_file))
    
    print(f'[ SUCCESS ] Static generation of \033[0;32m\'{BASE_DIRECTORY}/exec.sh\'\033[0;m completed at \033[0;32m{datetime.now()}\033[0;m',
        'Execute: \033[0;32m\'./exec.sh\'\033[0;m to initiate chrome remote debugging browser', sep='\n')


def create_driver_path(): # function used for adding steadycook driver_path
    # webdriver directory contains the absolute path to the chrome/firefox web drivers
    # drivers should stay in the local directory and not be accessed across the filesystem
    global BASE_DIRECTORY

    # dont need to have the below code for the function, in fact this function could be less than 4 lines
    # its better to define the driver_path so errors dont arise when users try to operate steadycook

    DRIVER_SOURCE_DIR = f'{BASE_DIRECTORY}/driver_src'
    WEBDRIVER_DIRECTORY = f'{os.path.join(DRIVER_SOURCE_DIR, "driver_path.txt")}' # /path/Project_SteadyCook/driver_src/driver_path.txt
    print('[+] OKAY: SteadyCook -> Writing path for webdriver() to \033[0;32m\'{}\'\033[0;m'.format(WEBDRIVER_DIRECTORY))
    
    with open(f'{WEBDRIVER_DIRECTORY}', 'w') as t_file:
        print(f'[ INFO ] Writing \'{DRIVER_SOURCE_DIR}\' into \'{WEBDRIVER_DIRECTORY}\'...')
        t_file.write(f'{DRIVER_SOURCE_DIR}/chrome_profile') # write the absolute path to the driver_src/*

    print(f'[+] Data written to \033[0;32m{WEBDRIVER_DIRECTORY}\033[0;m at \033[0;32m{datetime.now()}\033[0;m')
    print(f'[+] If you need to use and or update existing drivers you can find the absolute path at: \033[0;32m{DRIVER_SOURCE_DIR}\033[0;m')
    time.sleep(1)

    # need to generate exec.sh
    exec_path = f'{WEBDRIVER_DIRECTORY}'
    with open(exec_path, 'r') as d:
        send_data = d.readline()

    # run config.py
    ''' 
    generate_exec() depends on generated components from config.py
    cannot execute setup.py fully without calling config.py, data requested from generate_exec() relies on config.py being pre-loaded early
    '''
    print('[+] Directly calling \'config.py\' to pre-load \'settings.ini\' configuration file')
    call_config_instance()
    print('[ OK ] Call for \'config.py\' finished. Generated \'settings.ini\' successfully')
    generate_exec(str(send_data)) # send /path/Project_SteadyCook/driver_src/chrome_profile

def setup_main():
    # get path for chrome debugging user profile
    global POS_VAL
    global KEY_STATUS
    global BASE_DIRECTORY
    
    print('[?] Press the \033[0;32m\'SHIFT\'\033[0;m key to continue')
    key_listener()
    
    if KEY_STATUS == 'clicked':
        chrome_path = str(input('Enter absolute path for Chrome Profile: '))

        # check if the current file exists
        if os.path.isfile(chrome_path) == 1: # file exists
            sys.exit(1)
            # script will never reach this point because python doesnt recognize an existing CHROME_PROFILE_PATH
        
        elif os.path.isfile(chrome_path) == 0: # user doesn't have custom $CHROME_PROFILE default to steadycook

            print('\033[0;33mWARNING\033[0;m: In order to set and use an existing custom google chrome profile path',
                'You must manually set and link CUSTOM_CHROME_PATH as an environment variable to your existing chrome profile', 
                'Then rewrite \033[0;33m\'--user-data-dir=$CUSTOM_CHROME_PATH\'\033[0;m inside of \033[0;32m\'exec.sh\'\033[0;m to use a custom chrome path', sep='\n')
            
            time.sleep(5)
            print(f'\n[ INFO ] No \033[0;33m$CUSTOM_CHROME_PROFILE\033[0;m path detected. Falling back to steadycook local driver path: \033[0;32m{BASE_DIRECTORY}/driver_src\033[0;m')
            create_driver_path()
        
        # setup and install pip3 dependencies
        print('\nInstallig pip3 SteadyCook package dependencies : Printing out packages that are required for base installation ->')
        with open(f'{BASE_DIRECTORY}/requirements.txt', 'r') as req:
            packages = req.readlines()

            for x in packages:
                print('\t- \033[0;32m{}\033[0;m'.format(x.strip("\n")))

            time.sleep(1)
            try:
                subprocess.call(f'pip3 install -r {BASE_DIRECTORY}/requirements.txt', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            except Exception as error:
                print('\n\033[0;33mFailed to successfully download the required packages for a stable steadycook environment (sys_exit_1)\033[0;m')
                print('Manually execute: \'pip3 install -r requirements.txt\' and try again')
                print(str(error))
                sys.exit(1)
            # pip3 install -r requirements.txt successful
            else:
                print('\n[ INFO ] Successfully installed the required python packages for a stable installation of SteadyCook')
                get_automation_instance()

setup_main()
