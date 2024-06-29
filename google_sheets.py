from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def get_service():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = '/path/to/service/account/credentials.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)
    return service

def update_google_sheet(file_path, output_path):
    SPREADSHEET_ID = 'your_spreadsheet_id'
    RANGE_NAME = 'Sheet1!A2:D'

    service = get_service()
    sheet = service.spreadsheets()

    values = [[file_path, output_path, 'Processed', '']]
    body = {'values': values}

    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='RAW', body=
