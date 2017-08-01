
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_row():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the values from a range of
    cells in:
    https://docs.google.com/spreadsheets/d/1oI0gf7m68ZrrL5ITTYYvxDdP8NzY5mwmlzb4Y3oGpjA/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1oI0gf7m68ZrrL5ITTYYvxDdP8NzY5mwmlzb4Y3oGpjA'
    columnRange = '2017 Jul-Dec!A2:H2'
    column_headings = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=columnRange).execute()
    column_values = column_headings.get('values', [])
    rowRange = '2017 Jul-Dec!A3:H3'
    row = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rowRange).execute()
    row_values = row.get('values', [])

    if not row_values:
        print('No data found.')
    else:
        print(column_values)
        print(row_values)

if __name__ == '__main__':
    get_row()
