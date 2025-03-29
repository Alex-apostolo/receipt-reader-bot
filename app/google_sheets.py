from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def write_to_sheet(creds: Credentials, data: dict):
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets().values()
    values = [
        [data["vendor"], data["date"], data["total"]] +
        [f'{item["name"]} ({item["qty"]}) - {item["price"]}' for item in data["items"]]
    ]
    sheet.append(
        spreadsheetId="your-spreadsheet-id",
        range="Sheet1!A1",
        body={"values": values},
        valueInputOption="RAW"
    ).execute()
