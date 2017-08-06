from __future__ import print_function
import httplib2
import os
import csv
import pandas as pd
import datetime

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

# csv_file_path = input("Submit your desired filepath: ")
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
s - sum some month
p - print all
'''

def handler():
    operation = input(menu)
    if operation == "c":
        sheet_to_csv_create()
    if operation == "u":
        sheet_to_csv_append()
    if operation == "s":
        sum_month()
    if operation == "p":
        print_all()

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

    if not sheetValues:
        print('No data found in the selected range.')
    else:
        with open(csv_file_path, "a") as csv_file:
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

# printing rows from selected month worked only with DictReader
def sum_month():
    month = input("Enter the month you'd like to sum (in mm format): ")
    month_rows = []

    data = pd.read_csv(csv_file_path)
    for row in data:
        row["date"] = datetime.datetime.strptime(row["date"], "%m-%d-%Y")
    selection = data.loc[data['date'].month==month]
    print(selection)
    # for row in data:
    #     row["date"] = datetime.datetime.strptime(row["date"], "%m-%d-%Y")
    #     if row['date'][%m] == month:
    #         month_rows.append(row)
    # print(row["date"], row['summary'], row["run"], row["bike"], row["sports"], row["yoga"], row["abs"], row["lift"])

    # with open(csv_file_path, "r") as csv_file:
    #     reader = csv.DictReader(csv_file)
        #print(header)
        # for row in reader:
        #     if row['date'][0:2] == month:
        #         month_rows.append(row)
        #         print(row["date"], row['summary'], row["run"], row["bike"], row["sports"], row["yoga"], row["abs"], row["lift"])

        # reader.next()
        # print(sum(float(x[2]) for x in reader))

        # totals = []
        # run_total = 0
        # bike_total = 0
        # sports_total = 0
        # yoga_total = 0
        # abs_total = 0
        # lift_total = 0
        # for row in month_rows:
        #     run_total += int(row[2])
        #     bike_total += int(row[3])
        #     sports_total += int(row[4])
        #     yoga_total += int(row[5])
        #     abs_total += int(row[6])
        #     lift_total += int(row[7])
        # totals.append(run_total)
        # totals.append(bike_total)
        # totals.append(sports_total)
        # totals.append(yoga_total)
        # totals.append(abs_total)
        # totals.append(lift_total)
        # print(totals)

def print_all():
    with open(csv_file_path, "r") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=["date", "summary", "run", "bike", "sports", "yoga", "abs", "lift"])
        print("Here's everything in your database:")
        #print(header)
        for row in reader:
            print(row["date"], row["run"], row["bike"], row["sports"], row["yoga"], row["abs"], row["lift"])

if __name__ == '__main__':
    handler()
