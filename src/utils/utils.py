import os
import json
import traceback
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


# Use a more permissive scope to allow for sending and modifying emails,
# which is required by the send_gmail_message tool.
# gmail.modify includes readonly, send, and more.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

SECRET_PATH = os.path.expanduser('~/run/secrets')
# Check if running in Docker with mounted secrets (Standard path is /run/secrets)
if os.path.exists('/run/secrets/token.json'):
    SECRET_PATH = '/run/secrets'

def generate_token():
  creds = None

  try:
    
    if os.path.exists(SECRET_PATH + '/token.json'):
      creds = Credentials.from_authorized_user_file(SECRET_PATH + '/token.json', SCOPES)

    if not creds or not creds.valid:
      if creds and creds.expire and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(SECRET_PATH + '/dogsjgp_dev_gcp_gmail_mcp_server.json', SCOPES)    
        creds = flow.run_local_server(port = 0)

      try:
        with open(SECRET_PATH + '/token.json','w') as token:
          token.write(creds.to_json())
          print('Successfully created token.json')
      except OSError:
        print('Warning: Could not save refreshed token (likely due to read-only secrets storage in Docker). Continuing with current session.')

  except FileNotFoundError as e:
    print('Error: Missing file. Please ensure credential.json is present. {}'.format(e))
    traceback.print_exc()
    raise ValueError('Error: Missing file. Please ensure credential.json is present. {}'.format(traceback.format_exc()))

  except json.JSONDecodeError as e:
    print('Error JSON file is corrupted or formatted incorrectly. {}'.format(e))
    traceback.print_exc()
    raise ValueError('Error JSON file is corrupted or formatted incorrectly. {}'.format(traceback.format_exc()))

  except Exception as e:
    print('An unexpected error ocurred during the OAuth flow. {}'.format(e))
    traceback.print_exc()
    raise ValueError('An unexpected error ocurred during the OAuth flow. {}'.format(traceback.format_exc()))

def get_oauth_token():
    """Helper to retrieve the valid access token for the server."""
    if os.path.exists(SECRET_PATH + '/token.json'):
        creds = Credentials.from_authorized_user_file(SECRET_PATH + '/token.json', SCOPES)
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                return None
        return creds.token if creds and creds.valid else None
    return None

if __name__  == '__main__':
  generate_token()
