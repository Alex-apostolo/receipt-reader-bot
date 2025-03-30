from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
from typing import Optional
from app.models.receipt import Receipt
from app.services.firestore_service import FirestoreService


class SheetsService:
    def __init__(self):
        self.service = None
        self.spreadsheet_id = None
        self.firestore_service = FirestoreService()

    def get_spreadsheet_url(self) -> Optional[str]:
        """Get the URL of the spreadsheet."""
        if not self.spreadsheet_id:
            return None
        return f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"

    def initialize(self, credentials: Credentials, user_id: str):
        """Initialize the Google Sheets service with credentials."""
        self.service = build("sheets", "v4", credentials=credentials)
        self._load_or_create_spreadsheet(user_id)

    def _load_or_create_spreadsheet(self, user_id: str):
        """Load existing spreadsheet ID or create a new one."""
        # Try to load existing spreadsheet ID from Firestore
        self.spreadsheet_id = self.firestore_service.get_spreadsheet_id(user_id)
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

        # Save spreadsheet ID to Firestore
        self.firestore_service.save_spreadsheet_id(user_id, self.spreadsheet_id)

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
            body=body,
        ).execute()
