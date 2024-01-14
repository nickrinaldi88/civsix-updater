
#!/usr/bin/python3

import os
import json
import time
from datetime import datetime, timedelta

from googleapiclient.discovery import build, MediaFileUpload
from google.oauth2 import service_account

import logging

import utils

# import emailer
from utils.emailer import Emailer

################################# EMAIL CONFIGURATION #################################
# get current datetime
current_datetime = datetime.now()
date_string = current_datetime.strftime("%m-%d-%Y %H:%M:%S")


smtp_port = 587 # TLS port
smtp_server = "smtp.gmail.com"

file_name = 'TEDDY ROOSEVELT 25 3040 BC.Civ6Save'

subject = f"CIV VI SAVE FILE SCRIPT LOG - {date_string}"

# check for a metadata change, if a change, upload file. Otherwise, don't

source_path = "/Users/nickrinaldi/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/Saves/Single/"

print(source_path + file_name)

# Getting the size of the file
file_size = os.path.getsize(source_path)
modification_time = os.path.getmtime(source_path)
creation_time = os.path.getctime(source_path)


modification_time = datetime.fromtimestamp(modification_time)

def work():

    # get smtp user + pass
    try:
        with open('secrets.json', 'r') as file:
            data = json.load(file)
        smtp_username = data['smtp_username']
        smtp_password = data['smtp_password']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error: ", e)
        logging.info("Error: ", e)

    emailer = Emailer(smtp_server, smtp_username, smtp_password, smtp_port)
    emailer.create_email()
    emailer.send_email()

    with open("files/last_mod_time.txt", 'w+') as file:
            # read last email times
        file.write(modification_time)


def check_time(mod_time):

    with open("files/last_mod_time.txt", 'r') as file:
            # read last email times
            last_mod_time = file.read()
            if mod_time != last_mod_time:
                work()
                file.write(str(mod_time))
                return True
            return False
