from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import json
from typing import Optional
from app.models.receipt import Receipt


class SheetsService:
    def __init__(self):
        self.service = None
        self.spreadsheet_id = None
        self.spreadsheet_file = "spreadsheet_id.json"

    def get_spreadsheet_url(self) -> Optional[str]:
        """Get the URL of the spreadsheet."""
        if not self.spreadsheet_id:
            return None
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"

    def initialize(self, credentials: Credentials):
        """Initialize the Google Sheets service with credentials."""
        self.service = build("sheets", "v4", credentials=credentials)
        self._load_or_create_spreadsheet()

    def _load_or_create_spreadsheet(self):
        """Load existing spreadsheet ID or create a new one."""
        if os.path.exists(self.spreadsheet_file):
            with open(self.spreadsheet_file, "r") as f:
                data = json.load(f)
                self.spreadsheet_id = data.get("spreadsheet_id")
                if self.spreadsheet_id:
                    return

        # Create new spreadsheet if none exists
        spreadsheet = {
            "properties": {"title": "Receipt Tracker"},
            "sheets": [
                {
                    "properties": {
                        "title": "Receipts",
                        "gridProperties": {"frozenRowCount": 1},
                    }
                }
            ],
        }

        spreadsheet = (
            self.service.spreadsheets()
            .create(body=spreadsheet, fields="spreadsheetId")
            .execute()
        )

        self.spreadsheet_id = spreadsheet.get("spreadsheetId")

        # Save spreadsheet ID
        with open(self.spreadsheet_file, "w") as f:
            json.dump({"spreadsheet_id": self.spreadsheet_id}, f)

        # Set up headers
        headers = [["Date", "Merchant", "Total", "Items", "Tax", "Payment Method"]]
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range="Receipts!A1:F1",
            valueInputOption="RAW",
            body={"values": headers},
        ).execute()

    def append_receipt(self, receipt: Receipt):
        """Append a receipt to the spreadsheet."""
        if not self.service or not self.spreadsheet_id:
            raise ValueError("SheetsService not initialized with credentials")

        values = [receipt.to_row()]
        body = {"values": values}

        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range="Receipts!A:F",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body,
        ).execute()