from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from typing import Dict, Any, List
from app.config import SPREADSHEET_ID


class SheetsService:
    def __init__(self):
        self.spreadsheet_id = SPREADSHEET_ID
        self.service = None

    def initialize(self, credentials: Credentials):
        """Initialize the Google Sheets service with credentials."""
        self.service = build("sheets", "v4", credentials=credentials)

    def append_receipt(self, receipt_data: Dict[str, Any]):
        """Append receipt data to the spreadsheet."""
        if not self.service:
            raise ValueError("Sheets service not initialized with credentials")

        # Prepare the row data
        row = [
            receipt_data.get("date", ""),
            receipt_data.get("merchant", ""),
            receipt_data.get("total", ""),
            receipt_data.get("items", ""),
            receipt_data.get("tax", ""),
            receipt_data.get("payment_method", ""),
        ]

        # Append to the spreadsheet
        body = {"values": [row]}

        self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range="Receipts!A:F",  # Adjust range as needed
            valueInputOption="RAW",
            body=body,
        ).execute()

    def get_receipts(self) -> List[Dict[str, Any]]:
        """Get all receipts from the spreadsheet."""
        if not self.service:
            raise ValueError("Sheets service not initialized with credentials")

        result = (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=self.spreadsheet_id,
                range="Receipts!A:F",  # Adjust range as needed
            )
            .execute()
        )

        values = result.get("values", [])
        if not values:
            return []

        # Convert rows to receipt dictionaries
        receipts = []
        for row in values[1:]:  # Skip header row
            receipt = {
                "date": row[0],
                "merchant": row[1],
                "total": row[2],
                "items": row[3],
                "tax": row[4],
                "payment_method": row[5],
            }
            receipts.append(receipt)

        return receipts
