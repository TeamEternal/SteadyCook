# SteadyCook ✅
Automatic [stressthem.to](https://stressthem.to/login) Account Manipulation Tool

##### Note: This tool can be used for malicious purposes and the devlopers are not responsible, and can't be held liable for any damage caused from the misuse of SteadyCook

SteadyCook is a browser *automation tool* that actively uses [Selenium](https://selenium.dev/) and cached XPath information to automate the **free-load** process that is required to keep accounts registered on [https://stressthem.to](https://stressthem.to) to be able to continuously iterate through [DNS](https://www.cloudflare.com/learning/dns/what-is-dns/) based attacks at remote targets.

---



### Installation:
> Additional setup and configuration for SteadyCook may be needed to run in a proper environment

#### SteadyCook was created in a Python3 virtual environment, and it should be cloned and used in one!

NOTE: In order for SteadyCook to work you need to install Google Chrome and edit your '*.bashrc*' or '*.zshrc*' file to add Google Chrome to your systems global path. You can do this by the following:
   * `export PATH=$YOUR_PATH_TO_GOOGLE_CHROME:$PATH`
   
Where '*YOUR_PATH_TO_GOOGLE_CHROME*' is the absolute path to your Google Chrome installation

Once you are finished execute: `source <YOUR_RC_FILE>`

If you can execute: `Google\ Chrome` without any errors, continue to step #1.

To setup and install SteadyCook properly initiate the following:

1. Install *[virtualenv](https://pypi.org/project/virtualenv/)* from your local pip3 package directory:
   * Python: `pip3 install virtualenv` | Linux: `sudo apt-get install virtualenv` | MacOS: `brew install virtualenv`
   
2. Setup a new virtual environment via virtualenv with access to global python system-site packages:
   * `virtualenv Project_SteadyCook --python=python3.6 --system-site-packages`

3. Change your current directory to the virtual environment 'Project_SteadyCook':
   * `cd Project_SteadyCook/ ; source bin/activate`

4. Clone SteadyCook and move all local files to your virtual environment
   * `git clone https://github.com/TeamEternal/SteadyCook.git`
   * `cd SteadyCook/ ; mv * ..` then execute `cd .. ; sudo rm -r SteadyCook/`
   
5. Install the pip package *pynput* and create a 'driver_path.txt' file in the driver_src/ directory
   * `pip3 install pynput ; touch driver_src/driver_path.txt`

6. Start main installation of SteadyCook that will generate 'settings.ini' and store the DEFAULT_CHROME_PATH
   * `python3 setup.py`

The last command will generate the following files:
   * *'exec.sh'* - Needed to launch and pass custom data to Google Chrome's remote debugging browser
   * *'settings.ini'* - Your configuration initialization file: Used to set custom paramaters to control SteadyCook

### Customization & More:

SteadyCook has various features that allow the end user to control SteadyCook's execution statements via local options.

With SteadyCook you can do the following:
   * Pass SteadyCook through a user-controlled proxy server to mask network traffic directly from [https://stressthem.to](https://stressthem.to)
   * Modify the local target address and local ports SteadyCook will use to connect to Google Chrome's remote debugging browser
   * Automate powerfull DNS based attacks against remote targets for 8 hours (unlimited via future release)
   * Automate login functionality to speed up program execution time

#### Note: If you chose 'no' for the '*Setup and enable automatic login functionality (default=no):*' and you want to enable automatic login functionality you need to do the following:

Change your current directory to the virtual environment you created earlier (Project_SteadyCook) and execute:
   * `touch clientauth.txt`
   * Store your Username and Password for [https://stressthem.to](https://stressthem.to) in the following order: $USERNAME:$PASSWORD
   * Edit the '*automate_stressthem_login*' option (which defaults to no) inside of 'settings.ini' to 'yes' and re-launch SteadyCook via `python3 steadycook.py`

### Usage:

> SteadyCook is still currently in the early stages of development and as such the core command is only supported!

After a successfull installation, you can now use SteadyCook as follows:
   * `./exec.sh`
   * In a separate window execute: `python3 steadycook.py -t <target> -p <int: default 80> -d <int: max 8> -x dns`

**Why do I need to run `./exec.sh` before I can use SteadyCook?**

- The file `exec.sh` contains a command that SteadyCook heavily relies on, without Google Chrome's remote debugging browswer SteadyCook will not function at all. If you try to initiate SteadyCook without launching Google's remote debugging browser, the script will buffer as it tries to connect to the local Google Chrome server and will not be able to establish a connection.

**How do I exit from my currently activated virtual environment?**

- To fully close your currently activated virtual environment you need to execute: `deactivate` via the command-line

### Currently supported arguments

1. `-t` - Specifies a remote target in the form of an IPv4 address to launch a DNS based attack on
2. `-p` - Specifies the target port that will be used when the remote attack is started
3. `-d` - The duration the attack will last until execution is stopped (MAX=8hrs)
4. `-x` - The type of attack to initiate against the remote target (SUPPORTED=DNS)

WARNING: The time based data that SteadyCook uses to print TIME_PASSED and TIME_LEFT is still actively being developed. You might see numbers in the form of minutes left without the amount of hours left or hours passed. SteadyCook will still FULLY execute the attack for the duration that YOU SET in hours (via `-d`) This change will come in a later version, as the core features of SteadyCook are guaranteed to fully work, once you have setup a proper environment
   

