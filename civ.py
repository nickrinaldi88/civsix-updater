
#!/usr/bin/python3

import os
import json
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build, MediaFileUpload
from google.oauth2 import service_account

# import emailer
from utils.emailer import Emailer

################################# EMAIL CONFIGURATION #################################
# get current datetime
current_datetime = datetime.now()
date_string = current_datetime.strftime("%m-%d-%Y %H:%M:%S")


file_name = ""


smtp_port = 587 # TLS port
smtp_server = "smtp.gmail.com"

file_name = 'TEDDY ROOSEVELT 25 3040 BC.Civ6Save'

subject = f"CIV VI SAVE FILE SCRIPT LOG - {date_string}"

# check for a metadata change, if a change, upload file. Otherwise, don't

source_path = "/Users/nickrinaldi/Library/Application Support/Sid Meier's Civilization VI/Sid Meier's Civilization VI/Saves/Single/"

print(source_path + file_name)
# Getting the size of the file
file_size = os.path.getsize(source_path)

print(file_size)

# # Getting the last modification time
# modification_time = os.path.getmtime(file_path)