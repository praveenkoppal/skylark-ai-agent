import os
import json
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

class SheetsClient:
    def __init__(self):
        creds_json = json.loads(os.environ["GOOGLE_CREDENTIALS"])
        creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
        self.client = gspread.authorize(creds)

    def read(self, sheet_name):
        sheet = self.client.open(sheet_name).sheet1
        return sheet.get_all_records(), sheet

    def update_pilot_status(self, pilot_name, new_status):
        records, sheet = self.read("Pilot_Roster")
        headers = sheet.row_values(1)
        status_col = headers.index("status") + 1

        for idx, row in enumerate(records, start=2):
            if row.get("name", "").lower() == pilot_name.lower():
                sheet.update_cell(idx, status_col, new_status)
                return True
        return False
