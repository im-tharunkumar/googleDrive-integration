# GoogleDrive Integration Project

## Project Overview

This Flask-based project integrates with Google Drive, providing users with seamless access to their Google Drive accounts. Upon accessing the `/home` endpoint, users will find instructions and a button to redirect to the Google authentication page. After authenticating the app with their Google Drive accounts, the app will create a folder named "Docuedge" if not present, set up a webhook for that folder, and download all existing files in that folder and its subfolders. Subsequently, whenever users upload files to the specified folder or its subfolders, the webhook will notify the app, which will then download and save the files locally.

## Google SSO Login and OAuth Flow

### Google SSO Login:

Google Single Sign-On (SSO) enables users to log in to your application using their Google credentials. This project leverages Google SSO to authenticate users and access their Google Drive.

### OAuth Flow:

The OAuth flow involves the following steps:
1. **User Requests Authorization:** Users click on the provided button, initiating the OAuth flow.
2. **Redirect to Google Authorization Page:** Users are redirected to Google's authorization page to grant access to their Google Drive.
3. **User Grants Permission:** Users grant permission, and Google provides an authorization code.
4. **Exchange Authorization Code for Tokens:** The app exchanges the authorization code for access and refresh tokens.
5. **Access Google Drive API:** The app uses the access token to make requests to the Google Drive API on behalf of the user.

### Google Drive API Services:

This project utilizes Google Drive API services to interact with users' Google Drive accounts. The required API scope for this app is `drive.file` and `drive.readonly`. While the app retrieves user information for potential signup procedures, the primary focus is on syncing files with the local system.

**Note:** Detailed signup procedures are not completed in this project, as the primary purpose revolves around Google Drive integration.

## Setting Up Google Drive API

### Step-by-Step Setup:

1. **Create Virtual Environment:**
    ```bash
    python -m venv venv
    ```

2. **Install Packages from Requirements.txt:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Download and Place Google API Credentials:**
    - Download the Google API credentials JSON file and place it in the `static/` directory.

4. **Configure Webhook URI:**
    - Change the webhook URI to your actual URI in `conf/app_config.py`.

5. **Create Empty JSON Files:**
    - Create empty JSON files in the following names:
        - `access_token.json`
        - `refresh_token.json`
        - `uuid.json`
        - `folder_id.json`
        - `watch_token.json`
    - These files will store user-related information before the first-time run.

6. **Run the Application:**
    ```bash
    python app.py
    ```

## Reference Links:

- [Google OpenID Connect](https://developers.google.com/identity/openid-connect/openid-connect#python)
- [Google Drive API - Push Notifications](https://developers.google.com/drive/api/guides/push)
- [Google Drive API - Changes: getStartPageToken](https://developers.google.com/drive/api/reference/rest/v3/changes/getStartPageToken)
- [Google Drive API - Changes: list](https://developers.google.com/drive/api/reference/rest/v3/changes/list)
