import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta

def fetch_valid_order_ids(sheet_url,sheet_id):
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.get_worksheet_by_id(sheet_id)
    all_rows = worksheet.get_all_values()
    data_rows = all_rows[1:]
    valid_order_id = []
    for row in data_rows:
        order_name = row[0].strip()
        valid_order_id.append(order_name) 
    return valid_order_id

