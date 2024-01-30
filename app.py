import json
import threading
import requests
from flask import Flask, request, render_template, session
from utils.common_utils import get_or_create_folder, find_email_by_channel_id, process_update
from flask_session import Session
from conf.app_config import AUTH_URI, TOKEN_INFO_URI, TOKEN_URI, CLIENT_ID, CLIENT_SECRET, \
    REDIRECT_URI, ACCESS_TOKEN_DATA, REFRESH_TOKEN_DATA, UUID_DATA


app = Flask(__name__)

app.secret_key = "tharun"

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False  # Session will be deleted when the browser is closed

Session(app)

@app.route('/home', methods=['GET'])
def home():
    try:
        auth_uri = f'{AUTH_URI}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.readonly profile email&access_type=offline&response_type=code'
        return render_template("welcome.html", AUTH_URI=auth_uri)
    except Exception as e:
        print("error", e)

@app.route('/auth')
def auth():
    try:
        authorization_code = request.args.get('code')
        data = {
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET,
        'redirect_uri':REDIRECT_URI
        }
        response = requests.post(TOKEN_URI, data=data).json()
        token_info = requests.get(TOKEN_INFO_URI, params={"id_token":response.get("id_token")}).json()
        session['email'] = token_info["email"]
        user_mail = session['email']

        threading.Thread(target=get_or_create_folder, args=(response["access_token"],user_mail,)).start() 

        with open("access_token.json","w") as f:
            ACCESS_TOKEN_DATA[user_mail] = response["access_token"]
            json.dump(ACCESS_TOKEN_DATA, f)
        with open("refresh_token.json",'w') as f:
            REFRESH_TOKEN_DATA[user_mail] = response["refresh_token"]
            json.dump(REFRESH_TOKEN_DATA, f)
        return 'Access Granted'
    except Exception as e:
        print("error", e)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if request.headers.get('X-Goog-Resource-State') == 'sync':
            return 'sync success', 200
        if request.headers.get('X-Goog-Resource-State') == 'update' and \
            request.headers.get('X-Goog-Changed') == 'children':
            # print(request.headers)
            print(request.headers.get('X-Goog-Channel-Id'))
            threading.Thread(target=process_update, args=(session['email'],)).start() 
        return "received", 200
    except Exception as e:
        print("error", e)

@app.before_request
def before_request():
    if 'email' not in session and 'X-Goog-Channel-Id' in request.headers:
        channel_id = request.headers['X-Goog-Channel-Id']
        email = find_email_by_channel_id(channel_id, uuid_data=UUID_DATA)
        if email:
            session['email'] = email
        else:
            return "channel ID not fount",200
