import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

def update_sheet_from_report(sheet_url, sheet_id, report_file):
    credentials = Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    client = gspread.authorize(credentials)

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