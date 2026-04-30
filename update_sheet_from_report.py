import smtplib
import requests
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleads import ad_manager
import gspread
import tempfile
import os
import gzip
import pandas as pd
import shutil
import datetime
import pytz
import csv
import json
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleads import errors
import logging
logging.basicConfig(level=logging.DEBUG)
from oauth2client.service_account import ServiceAccountCredentials

def update_sheet_from_report(sheet_url, sheet_id, report_file):
    creds_json = json.loads(GOOGLE_CREDENTIALS_JSON)
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.get_worksheet_by_id(sheet_id)

    sheet_data = worksheet.get_all_values()

    # Map Column A → row index
    sheet_map = {}
    for i in range(1, len(sheet_data)):
        key = sheet_data[i][0].strip()
        sheet_map[key] = i

    df = pd.read_csv(report_file)

    # Prepare only I & J columns
    updates = []

    for _, row in df.iterrows():
        order_name = str(row['Dimension.ORDER_NAME']).strip()

        imp = row.get('Column.AD_SERVER_IMPRESSIONS', 0)
        clicks = row.get('Column.AD_SERVER_CLICKS', 0)
        viewable_imps=row.get('Column.AD_SERVER_ACTIVE_VIEW_VIEWABLE_IMPRESSIONS',0)
        reach=row.get('Column.UNIQUE_REACH',0)

        if order_name in sheet_map:
            idx = sheet_map[order_name] + 1  # sheet row number

            updates.append({
            'range': f'I{idx}:J{idx}',
            'values': [[imp, clicks]]
        })

            updates.append({
            'range': f'T{idx}',
            'values': [[viewable_imps]]
        })
            updates.append({
            'range': f'V{idx}',
            'values': [[reach]]
        })

            print(f"Prepared update {order_name}")
        else:
            print(f"Not found {order_name}")

    #  Batch update only required cells
    if updates:
        worksheet.batch_update(updates)

    print(" Bulk update completed")
