from __future__ import print_function
import httplib2
import os
import csv
import pandas as pd
from datetime import datetime
from dateutil.parser import parse

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from IPython import embed

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Print Range from Google Sheet'

csv_file_path = "data/all_workouts.csv"

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

menu = '''
Please pick the letter corresponding to the operation that you would like to conduct on the fitness database:
c - create
u - update
s - select from range
p - print all
+ - sum range
x - exit
'''
operations = ["c", "u", "s", "p", "+", "x"]

def handler(): # for production version, make sure while loop is active
    x = 0
    while x ==0:
        operation = input(menu)
        if operation == "c":
            sheet_to_csv_create()
        if operation == "u":
            sheet_to_csv_append()
        if operation == "s":
            select_range()
        if operation == "p":
            print_all()
        if operation == "x":
            x = 1
        if operation == "+":
            sum_range()
        if operation not in operations:
            print("I'm sorry, I didn't recognize that operation, please try another:")

def sheet_to_csv_create():
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

    sheetRange = input("Enter the sheet name and cell range (in A1 format like this without quotation marks - sheet_name!A3:H28): ")
    #sheetRange = '2017 Jul-Dec!A3:H28'
    sheetData = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=sheetRange).execute()
    sheetValues = sheetData.get('values', [])

    csv_create_path = input("Submit your desired filepath starting with data/: ")

    if not sheetValues:
        print('No data found.')
    else:
        with open(csv_create_path, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["date", "summary", "run", "bike", "sports", "yoga", "abs", "lift"])
            writer.writeheader()
            for row in sheetValues:
                for i in [0,1,2,3,4,5,6,7]:
                    try:
                        if not row[i]:
                            row[i] = 0
                    except IndexError as e:
                        row.append(0)
                workout = {
                "date": row[0],
                "summary": row[1],
                "run": row[2],
                "bike": row[3],
                "sports": row[4],
                "yoga": row[5],
                "abs": row[6],
                "lift": row[7]
                }
                writer.writerow(workout)

def sheet_to_csv_append():
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

    sheetRange = input("Enter the sheet name and cell range (in A1 format like this without quotation marks - sheet_name!A3:H28): ")
    #sheetRange = '2017 Jul-Dec!A3:H28'
    sheetData = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=sheetRange).execute()
    sheetValues = sheetData.get('values', [])

    csv_update_path = input("Submit your desired filepath starting with data/: ")

    if not sheetValues:
        print('No data found in the selected range.')
    else:
        with open(csv_update_path, "a") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["date", "summary", "run", "bike", "sports", "yoga", "abs", "lift"])
            #writer.writeheader()
            print("Here's the data you just added to your database:")
            for row in sheetValues:
                for i in [0,1,2,3,4,5,6,7]:
                    try:
                        if not row[i]:
                            row[i] = 0
                    except IndexError as e:
                        row.append(0)
                print(row)
                workout = {
                "date": row[0],
                "summary": row[1],
                "run": row[2],
                "bike": row[3],
                "sports": row[4],
                "yoga": row[5],
                "abs": row[6],
                "lift": row[7]
                }
                writer.writerow(workout)

def select_range():
    first_date = input("Enter the first day of the period you'd like to display (format = 'yyyy-mm-dd'): ")
    last_date = input("Enter the last day of the period you'd like to display (format = 'yyyy-mm-dd'): ")

    data = pd.read_csv(csv_file_path)
    data['date'] = pd.to_datetime(data['date'])
    data.index = data['date']
    data.drop(['date'], axis=1, inplace=True)
    selection = data.ix[first_date:last_date]
    print(selection)

def sum_range():
    # first_date = '2017-01-01'
    # last_date = '2017-01-31'
    first_date = input("Enter the first day of the period you'd like to sum (format = 'yyyy-mm-dd'): ")
    last_date = input("Enter the last day of the period you'd like to sum (format = 'yyyy-mm-dd'): ")

    # selecting the rows
    data = pd.read_csv(csv_file_path)
    data['date'] = pd.to_datetime(data['date'])
    data.index = data['date']
    data.drop(['date'], axis=1, inplace=True)
    selection = data.ix[first_date:last_date]

    # totaling the selected rows
    totals = []
    run_total = selection['run'].sum(axis=0)
    bike_total = selection['bike'].sum(axis=0)
    sports_total = selection['sports'].sum(axis=0)
    yoga_total = selection['yoga'].sum(axis=0)
    abs_total = selection['abs'].sum(axis=0)
    lift_total = selection['lift'].sum(axis=0)
    totals.append("Totals: ")
    totals.append(run_total)
    totals.append(bike_total)
    totals.append(sports_total)
    totals.append(yoga_total)
    totals.append(abs_total)
    totals.append(lift_total)
    print(totals)

def print_all():
    #csv_print_path = input("Submit the filepath of the csv you previously created,starting with data/: ")
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=["date", "summary", "run", "bike", "sports", "yoga", "abs", "lift"])
        print("Here's everything in your database:")
        for row in reader:
            print(row["date"], row["run"], row["bike"], row["sports"], row["yoga"], row["abs"], row["lift"])

if __name__ == '__main__':
    handler()
