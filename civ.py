
#!/usr/bin/python3

import os
import json
import time
from datetime import datetime, timedelta

from googleapiclient.discovery import build, MediaFileUpload
from google.oauth2 import service_account

import logging
import mimetypes

# import emailer
import utils
from utils.emailer import Emailer

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

################################# EMAIL CONFIGURATION #################################
# get current datetime
current_datetime = datetime.now()
date_string = current_datetime.strftime("%m-%d-%Y %H:%M:%S")


smtp_port = 587 # TLS port
smtp_server = "smtp.gmail.com"

file_name = 'TEDDY ROOSEVELT 25 3040 BC.Civ6Save'

subject = f"CIV VI SAVE FILE SCRIPT LOG - {date_string}"
# scope
scopes = ['https://www.googleapis.com/auth/drive']

# check for a metadata change, if a change, upload file. Otherwise, don't

source_path = "/Users/nickrinaldi/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/Saves/Single/"
credentials_path = 'creds/service_account_key.json'
raw_path = source_path + file_name

# Getting the size of the file
file_size = os.path.getsize(source_path)
mod_time = os.path.getmtime(source_path)
creation_time = os.path.getctime(source_path)


mod_datetime = datetime.fromtimestamp(mod_time)
dash = "-"
# build heartbeat 
def log_heartbeat():

    logging.info(f"INTERNAL LOG: File upload at {mod_datetime}")
    logging.info(dash * 25)

def build_drive_service(credentials_path, scopes):

    creds = None

    try:
        creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=scopes)
    except Exception as e:
        print(f"Error intializing service account creds. Exception: {e}")
        logging.error(f"Error intializing service account creds. Exception: {e}")

    drive_service = build('drive', 'v3', credentials=creds)
    return drive_service

def work():

    # get smtp user + pass
    try:
        with open('creds/secrets.json', 'r') as file:
            data = json.load(file)
        smtp_username = sender_email = receiver_email = data['smtp_username']
        print(smtp_username)
        smtp_password = data['smtp_password']
            # folder id
        folder_id = data['folder_id']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error: ", e)
        logging.info("Error: ", e)

    # build the drive service
    drive_service = build_drive_service(credentials_path, scopes=scopes)

    # create file object
    file_metadata = {
        'raw_path':  raw_path,
        'name': file_name,
        'parents': [folder_id]
    }

    mime_type, _ = mimetypes.guess_type(file_metadata['raw_path'])
    media = MediaFileUpload(file_metadata['raw_path'], mimetype=mime_type, resumable=True)
    request = drive_service.files().create(
        body=file_metadata,
        media_body = media,
        fields='id'
    )

    # INSTANIATE EMAILER

    body = f"The script uploaded a save file today at {mod_datetime}"
    attachment_path = "logs/heartbeat.log"

    log_heartbeat()

    emailer = Emailer(smtp_server, smtp_username, smtp_password, smtp_port)
    email = emailer.create_email(sender_email, receiver_email, subject, body, attachment_path, mod_datetime)

        # send email 
    emailer.send_email(sender_email, receiver_email, email)

    # OPEN MOD TIME, WRITE NEW MOD TIME

    with open("files/last_mod_time.txt", 'w+') as file:
            # read last email times
        mod_time = file.read()
        print(mod_time)
        
        mod_time = str(mod_time)
        file.write(mod_time)


def check_time(mod_time):

    with open("files/last_mod_time.txt", 'r+') as file:
            # read last email times
            last_mod_time = file.read()

            if mod_time != last_mod_time:
                work()
                return True
            return False

check_time(mod_time)