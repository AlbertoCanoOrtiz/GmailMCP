import os
import json
import traceback
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SECRET_PATH = os.path.expanduser('~/run/secrets')

def generate_token():
  creds = None

  try:
    
    if os.path.exists(SECRET_PATH + '/token.json'):
      creds = Credentials-from_authorized_user_file(SECRET_PATH + '/token.json', SCOPES)

    if not creds or not creds.valid:
      if creds and creds.expire and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(SECRET_PATH + '/dogsjgp_dev_gcp_gmail_mcp_server.json', SCOPES)    
        creds = flow.run_local_server(port = 0)

      with open(SECRET_PATH + '/token.json','w') as token:
        token.write(creds.to_json())
        print('Successfully created token.json')

  except FileNotFoundError as e:
    print('Error: Misssing file. Please ensure credential.json is present. {}'.format(e))
    traceback.print_exc()
    raise ValueError('Error: Misssing file. Please ensure credential.json is present. {}'.format(traceback.print_exc()))

  except json.JSONDecodeError as e:
    print('Error JSON file is corrupted or formatted incorrectly. {}'.format(e))
    traceback.print_exc()
    raise ValueError('Error JSON file is corrupted or formatted incorrectly. {}'.format(traceback.print_exc()))

  except Exception as e:
    print('An unexpected error ocurred during the OAuth flow. {}'.format(e))
    traceback.print_exc()
    raise ValueError('An unexpected error ocurred during the OAuth flow. {}'.format(traceback.print_exc()))

if __name__  == '__main__':
  generate_token()
