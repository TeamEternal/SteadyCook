import os
import sys
import time
import tabulate
import argparse
import cook_handler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 


# setup.py exec.sh, auto_login, 

# create file for chrome debugging startup, ask for path, etc.
# use token file to verify wether or not the user has an account
# if the user doesn't have an active account, use temp-mail API to gen email
# and generate a weak random password (throw away account)

# give the option to automatically have steadycook automate login for the client
# captcha might have to be filled out but that is not a problem


# set banner as an option
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

# make definition for input
def program_input():
      pass
    

# make definition to handle program flow
def main_execution(comm):
      pass


if __name__ == '__main__':
      # setup and define CLI based flags
      formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=52)
      parser = argparse.ArgumentParser(prog='SteadyCook', description='automatic stressthem.to account manipulation tool',
                                          formatter_class=formatter)

      meta_ch = 'X'

      parser.add_argument('-t', '--target', help='define remote host (IPv4 format only)', metavar=meta_ch)
      parser.add_argument('-p', '--port', help='set reserved or dynamic/private port', metavar=meta_ch)

      # add later feature to set minutes, hours, etc
      parser.add_argument('-d', '--duration', help='interval for time-based duration', metavar=meta_ch)
      parser.add_argument('-x', '--type', help='define method of execution against target/host', metavar=meta_ch)
      parser.add_argument('--show-targets', help='request list of unique past targets (max 25)', action='store_true')
      parser.add_argument('-r', '--request-info', help='request info from Shodan about the target', metavar=meta_ch)
      parser.add_argument('--export-db', help='export hosts from $SET_FILE parameter', metavar=meta_ch)
      parser.add_argument('--execute-cli', help='drop into a CLI based environment', action='store_true')
      parser.add_argument('-I', '--infinite', help='launch automated attack continuously until SIGINT returned', action='store_true')
      parser.add_argument('--banner', help='display the SteadyCook CLI banner and exit', action='store_true')

      args = parser.parse_args()

      # define base parameters that would be needed to launch SC
      host_info = [args.target, args.port, args.duration, args.type]
      completed_commands = [args.target, args.port, args.duration, args.type, args.banner]

      # setup and initiate methods for handling multiple arguments
      if all(host_info):
            # max time limit for this tool & version should be no more than 6 hours
            if int(args.duration) > 8:
                  print('Recieved: %s' % args.duration)
                  parser.error('[ \033[0;31mEXEC_ERROR\033[0;m ] => Max attack duration is 8 hours (sys_exit_1) Aborting...')
            
            elif str(args.type.lower()) != 'dns':
                  print('Recieved: %s' % args.type)
                  parser.error('[ \033[0;31mEXEC_ERROR\033[0;m ] => SteadyCook only supports DNS based attacks (sys_exit_1) Aborting...')
            else:
                  print(f'Target: \033[0;32m{args.target}\033[0;m', f'Port: \033[0;32m{args.port}\033[0;m', 
                        f'Duration: \033[0;32m{args.duration}\033[0;m', f'Type: \033[0;32m{args.type}\033[0;m', sep='\n')

                  # pass information to cook_handler function
                  cook_handler.parse_host_info(args.target, args.port, args.duration, args.type)
      
      # if the user has requested for the terminal to print out the banner
      elif args.banner:
            print(banner)

      else:
            parser.print_help()
            exit()

else:
      print('[ \033[0;31mERROR\033[0;m ] The program you are calling was NOT intended to be imported (sys_exit_1)')
      sys.exit(1)