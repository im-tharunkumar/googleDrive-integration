import uuid
import os
import requests
import json
from datetime import datetime, timedelta
from conf.app_config import WATCH_TOKEN_DATA, UUID_DATA, SAVE_PATH, DRIVE_API_URL, ACCESS_TOKEN_DATA, FOLDER_DATA, WEBHOOK_URL

def create_folder(access_token):
    folder_data = {
        'name': 'Docuedge',  # Replace with your app name
        'mimeType': 'application/vnd.google-apps.folder',
    }
    headers = {'Authorization': f'Bearer {access_token}'}
    create_folder_url = f'{DRIVE_API_URL}/files'
    folder_response = requests.post(create_folder_url, headers=headers, json=folder_data).json()
    return folder_response['id']

def set_webhook(resource_id, access_token, user_mail):
    if user_mail not in UUID_DATA:
          UUID_DATA[user_mail] = []
    unique_channel_id = str(uuid.uuid4())
    current_time = datetime.now()
    new_time = current_time + timedelta(hours=1)
    new_time = int(new_time.timestamp()*1000)
    notification_channel = {
        "id": unique_channel_id,
        "type": "web_hook",
        "address": WEBHOOK_URL,
        "expiration": new_time,
    }
    api_url = f'https://www.googleapis.com/drive/v3/files/{resource_id}/watch'
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    response = requests.post(api_url, headers=headers, data=json.dumps(notification_channel))
    get_start_token_url = "https://www.googleapis.com/drive/v3/changes/startPageToken"
    response = requests.get(get_start_token_url, headers=headers).json()
    # print(user_mail,response["startPageToken"])
    with open("watch_token.json", "w") as f:
        WATCH_TOKEN_DATA[user_mail] = response["startPageToken"]
        json.dump(WATCH_TOKEN_DATA, f)
    # print("watch token set")
    UUID_DATA[user_mail].append(unique_channel_id)

    with open("uuid.json", "w") as f:
        json.dump(UUID_DATA, f)
    if user_mail not in FOLDER_DATA:
        FOLDER_DATA[user_mail] = []
    FOLDER_DATA[user_mail].append(resource_id)
    with open("folder_id.json",'w') as f:
        json.dump(FOLDER_DATA, f)
    print("webhok set ", resource_id)


def find_email_by_channel_id(channel_id, uuid_data):
    for email, channel_ids in uuid_data.items():
        # print(email, channel_ids)
        if channel_id in channel_ids:
            return email
    return None



# Function to check if a folder already exists in the Google Drive home directory
def get_or_create_folder(access_token, user_mail):
    folder_name = 'Docuedge'  # Replace with your app name
    headers = {'Authorization': f'Bearer {access_token}'}
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    search_url = f'{DRIVE_API_URL}/files?q={query}'
    search_response = requests.get(search_url, headers=headers).json()
    if 'files' in search_response and search_response['files']:
        folder_id = search_response['files'][-1]['id']
        set_webhook(folder_id, access_token, user_mail)
        download_existing_files(access_token=access_token, folder_id=folder_id, user_mail=user_mail)
    else:
        folder_id = create_folder(access_token)
        set_webhook(folder_id, access_token, user_mail)
    
    # with open("folder_id.json",'w') as f:
    #     json.dump(FOLDER_DATA, f)

def download_existing_files(access_token, folder_id, user_mail):
    # Perform a query to get all files within the specified folder
    files_query = f'"{folder_id}" in parents'
    files_url = f'{DRIVE_API_URL}/files?q={files_query}'
    files_response = requests.get(files_url, headers={'Authorization': f'Bearer {access_token}'}).json()
    # print("download exist:" ,files_response)
    # print(files_response)
    # abort(404)

    # Iterate through the files and download each one
    for file_info in files_response.get('files', []):
        file_id = file_info['id']
        file_name = file_info['name']
        file_mimeType = file_info["mimeType"]
        if file_mimeType not in ['application/vnd.google-apps.folder']:
            download_url = f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media'
            file_content = requests.get(download_url, headers={'Authorization': f'Bearer {access_token}'}).content
            user_save_path = os.path.join(SAVE_PATH, user_mail)
            os.makedirs(user_save_path, exist_ok=True)

            # Save the file locally
            local_file_path = os.path.join(user_save_path, file_name)
            with open(local_file_path, 'wb') as local_file:
                local_file.write(file_content)
        elif file_mimeType in ['application/vnd.google-apps.folder'] and file_id not in FOLDER_DATA[user_mail]:
            set_webhook(file_id,access_token,user_mail)
            download_existing_files(access_token=access_token,folder_id=file_id,user_mail=user_mail)

        # print(f"Downloaded file: {file_name}")
def process_update(user_mail):
    change_url ="https://www.googleapis.com/drive/v3/changes"
    notification_channel = {
            "pageToken":WATCH_TOKEN_DATA[user_mail]
            }
    
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN_DATA[user_mail]}', 'Content-Type': 'application/json'}
    response = requests.get(change_url, headers=headers, params=notification_channel).json()
    print("inside process update", response)

    mime_types_not_to_download = ['application/vnd.google-apps.folder']
    # print(response["changes"])
        #   print(response)
    for each_file in response["changes"]:
        if not each_file['removed']:
            file_id = each_file["file"]["id"] 
            file_name = each_file["file"]["name"] 
            file_mimeType = each_file["file"]["mimeType"]
            parents_url = f'https://www.googleapis.com/drive/v3/files/{file_id}?fields=parents'
            parents_response = requests.get(parents_url, headers=headers).json()
            # print(parents_response, file_id)
            if parents_response['parents'][0] in FOLDER_DATA[user_mail]:
                if file_mimeType not in mime_types_not_to_download:
                    download_url = f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media'
                    file_content = requests.get(download_url, headers=headers).content

                    # Create user-specific directory if it doesn't exist
                    user_save_path = os.path.join(SAVE_PATH, user_mail)
                    os.makedirs(user_save_path, exist_ok=True)

                    # Save the file locally
                    local_file_path = os.path.join(user_save_path, file_name)
                    with open(local_file_path, 'wb') as local_file:
                        local_file.write(file_content)
                elif file_mimeType in mime_types_not_to_download and file_id not in FOLDER_DATA[user_mail]:
                    # print(file_id,file_id not in FOLDER_DATA[user_mail] )
                    set_webhook(file_id,access_token=ACCESS_TOKEN_DATA[user_mail], user_mail=user_mail)
    with open("watch_token.json","w") as f:
        WATCH_TOKEN_DATA[user_mail] = response["newStartPageToken"]
        json.dump(WATCH_TOKEN_DATA, f)