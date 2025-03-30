from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.models.receipt import Receipt
from app.config import SPREADSHEET_ID


class SheetsService:
    def __init__(self):
        self.spreadsheet_id = SPREADSHEET_ID
        self.sheets_service = None
        self.headers = ["Date", "Merchant", "Total", "Items", "Tax", "Payment Method"]

    def initialize(self, credentials: Credentials):
        """Initialize the Google Sheets service with user credentials."""
        self.sheets_service = build("sheets", "v4", credentials=credentials)
        self._ensure_headers()

    def _ensure_headers(self):
        """Ensure the spreadsheet has the correct headers."""
        try:
            # Check if headers exist
            result = (
                self.sheets_service.spreadsheets()
                .values()
                .get(spreadsheetId=self.spreadsheet_id, range="Sheet1!A1:F1")
                .execute()
            )

            if not result.get("values"):
                # Add headers if they don't exist
                self.sheets_service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range="Sheet1!A1:F1",
                    valueInputOption="RAW",
                    body={"values": [self.headers]},
                ).execute()
        except Exception as e:
            print(f"Error ensuring headers: {str(e)}")
            raise

    def append_receipt(self, receipt: Receipt):
        """Append a receipt to the spreadsheet."""
        if not self.sheets_service:
            raise ValueError("Sheets service not initialized")

        # Convert receipt to row format
        row = receipt.to_row()

        # Append the row to the spreadsheet
        body = {"values": [row]}
        self.sheets_service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range="Sheet1!A:F",  # Adjust range to include all columns
            valueInputOption="RAW",
            body=body,
        ).execute()
