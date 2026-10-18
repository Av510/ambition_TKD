import os
import sqlite3
from datetime import datetime

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# SETTINGS

DATABASE = "/home/daia12345/ambition_TKD/attendance_tracker/TKD.db"

BACKUP_FOLDER = "/home/daia12345/ambition_TKD/backups"

TOKEN_FILE = "/home/daia12345/ambition_TKD/token.json"

DRIVE_FOLDER_ID = "171-Np8Oa0PYtJL1luZYruTW1JKNng8R6"

SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]


# CREATE LOCAL BACKUP

def create_backup():

    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    date = datetime.now().strftime("%Y-%m-%d")

    backup_path = os.path.join(
        BACKUP_FOLDER,
        f"TKD_backup_{date}.db"
    )

    source = sqlite3.connect(DATABASE)

    backup = sqlite3.connect(backup_path)

    with backup:
        source.backup(backup)

    source.close()
    backup.close()

    print(f"Backup created: {backup_path}")

    return backup_path


# CONNECT TO GOOGLE DRIVE

def get_drive_service():

    creds = Credentials.from_authorized_user_file(
        TOKEN_FILE,
        SCOPES
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build(
        "drive",
        "v3",
        credentials=creds
    )


# UPLOAD BACKUP

def upload_to_drive(file_path):

    service = get_drive_service()

    file_name = os.path.basename(file_path)

    file_metadata = {
        "name": file_name,
        "parents": [DRIVE_FOLDER_ID]
    }

    media = MediaFileUpload(
        file_path,
        mimetype="application/x-sqlite3"
    )

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,name"
    ).execute()

    print(
        f"Uploaded: {uploaded_file['name']}"
    )


# MAIN

if __name__ == "__main__":

    backup_file = create_backup()

    upload_to_drive(backup_file)

    print("Backup completed successfully!")
