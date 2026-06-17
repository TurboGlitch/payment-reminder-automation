import gspread
from google.oauth2.service_account import Credentials


def get_pending_clients():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.readonly"
    ]
    creds = Credentials.from_service_account_file("service_account.json", scopes=scopes)
    client = gspread.authorize(creds)

    sheet = client.open("data").sheet1
    data = sheet.get_all_records()

    # print(data)

    pending = []
    for i, row in enumerate(data):
        if row["Status"] in ["Pending", "Overdue"]:
            row["row_number"] = i + 2 # +2 because row 1 is headers, and sheets are 1-indexed
            pending.append(row)

    return pending, sheet


def mark_as_reminded(sheet, row_number, status_column=8):
    sheet.update_cell(row_number, status_column, "Reminded")

