import os
import json

with open(os.path.join(os.getcwd(), 'access_token.json')) as f:
    ACCESS_TOKEN_DATA = json.load(f)
with open(os.path.join(os.getcwd(), 'refresh_token.json')) as f:
    REFRESH_TOKEN_DATA = json.load(f)
with open(os.path.join(os.getcwd(), 'folder_id.json')) as f:
    FOLDER_DATA = json.load(f)
with open(os.path.join(os.getcwd(), 'watch_token.json')) as f:
    WATCH_TOKEN_DATA = json.load(f)
with open(os.path.join(os.getcwd(), 'uuid.json')) as f:
    UUID_DATA = json.load(f)
with open('static\client_secret_610599435431-179692j28ic1j47cr0eoreseckuhqai0.apps.googleusercontent.com.json') as f:
    GOOGLE_API_DATA = json.load(f)

# class Config(object):
GOOGLE_API_DATA = GOOGLE_API_DATA
ACCESS_TOKEN_DATA = ACCESS_TOKEN_DATA
REFRESH_TOKEN_DATA = REFRESH_TOKEN_DATA
FOLDER_DATA = FOLDER_DATA
WATCH_TOKEN_DATA = WATCH_TOKEN_DATA
UUID_DATA = UUID_DATA
AUTH_URI = GOOGLE_API_DATA["web"]["auth_uri"]
TOKEN_URI = GOOGLE_API_DATA["web"]["token_uri"]
TOKEN_INFO_URI = "https://oauth2.googleapis.com/tokeninfo"
CLIENT_ID = GOOGLE_API_DATA["web"]["client_id"]
CLIENT_SECRET = GOOGLE_API_DATA["web"]["client_secret"]
REDIRECT_URI = GOOGLE_API_DATA["web"]["redirect_uris"][0]

WEBHOOK_URL = "https://a962-115-160-253-98.ngrok-free.app/webhook"
SAVE_PATH = "save_files"
DRIVE_API_URL = 'https://www.googleapis.com/drive/v3'

# def get_config():
#     if os.environ['ENV'] == 'dev':
#         return Config()