from fetch_valid_order_names import fetch_valid_order_ids
from googleads import ad_manager
from update_sheet_from_report import update_sheet_from_report
from impressions_clicks_of_order import download_combined_report_by_name
sheet_url = "https://docs.google.com/spreadsheets/d/1u68QXESgLIlfDHzSY_9QVCd9pFIk-sCqiSBB9IERz9g/edit?gid=1080823886#gid=1080823886"
sheet_id=1080823886
client= ad_manager.AdManagerClient.LoadFromStorage('googleads1.yaml')

if __name__ == '__main__':
    order_names = fetch_valid_order_ids(sheet_url, sheet_id)
    report_file = download_combined_report_by_name(client, order_names) 
    print(report_file)

    if report_file:
        update_sheet_from_report(sheet_url, sheet_id, report_file)


         
            
    
    