import os
import sys
import configparser

config = configparser.ConfigParser()
LOCAL_DIRECTORY_BASENAME = os.path.basename(os.getcwd())

def call_config_instance():
    with open('settings.ini', 'w') as f:
        config.write(f)

if LOCAL_DIRECTORY_BASENAME == 'Project_SteadyCook':

    config['PATHS'] = {
        'driver_src_path' : f'{os.getcwd()}/driver_src', # default path for drivers
        'default_chrome_path' : f'{os.getcwd()}/driver_src/chrome_profile' # set path for default chrome profile
    }

    config['TARGETS'] = {
        'unauthorized_url' : 'https://www.stressthem.to/login',
        'authorized_url'   : 'https://www.stressthem.to/booter'
    }

    config['DEBUGGER_SETTINGS'] = {
        'target_port' : '9222',
        'target_address' : '127.0.0.1'
    }

    config['AUTOMATION_OPTIONS'] = {
        'automate_stressthem_login' : 'no', # default value
        'custom_chrome_profile' : ''
    }

else:
    print('[ STATUS ] Trouble trying to generate \'settings.ini\', change your directory to \'Project_SteadyCook\' and try again')
    sys.exit(1)