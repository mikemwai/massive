import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# fetch email
file_path = "email.txt"
try:
    with open(file_path, "r") as file:
        my_email = file.read()
except FileNotFoundError:
    print(f"File not found: {file_path}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

credentials = service_account.Credentials.from_service_account_file('cohesive-scope-400809-b4cb18e44e7b.json',
                                                                    scopes=['https://www.googleapis.com/auth/drive'])

drive_service = build('drive', 'v3', credentials=credentials)

project_folder_path = 'C:/Users/Usewr/computer_graphics/massive'


def upload_file(file_path, parent_folder_id):
    filename = os.path.basename(file_path)
    file_metadata = {
        'name': filename,
        'parents': [parent_folder_id]
    }
    media = MediaFileUpload(file_path)
    drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()


folder_metadata = {
    'name': 'Computer Graphics GRP9',
    'mimeType': 'application/vnd.google-apps.folder'
}
folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
folder_id = folder.get('id')

permission = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': my_email
}
drive_service.permissions().create(fileId=folder_id, body=permission).execute()

for root, dirs, files in os.walk(project_folder_path):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        if '.git' not in file_path:
            upload_file(file_path, folder_id)

print('Project folder uploaded successfully and shared with precious.boruett@strathmore.edu.')
