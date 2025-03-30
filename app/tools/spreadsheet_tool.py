from typing import Dict, Any, List
from app.models.receipt import Receipt
from app.services.sheets_service import SheetsService
from app.services.google_service import GoogleService


class SpreadsheetTool:
    def __init__(self, google_service: GoogleService):
        self.google_service = google_service
        self.sheets_service = None

    @property
    def function_schema(self) -> List[Dict[str, Any]]:
        """Get the function schema for the LLM."""
        return [
            {
                "name": "add_receipt",
                "description": "Add a receipt to the spreadsheet",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "Date in MM/DD format",
                        },
                        "merchant_name": {
                            "type": "string",
                            "description": "Name of the merchant",
                        },
                        "total_amount": {
                            "type": "number",
                            "description": "Total amount of the receipt",
                        },
                        "items_purchased": {
                            "type": "array",
                            "description": "List of items purchased with prices",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Name of the item",
                                    },
                                    "price": {
                                        "type": "number",
                                        "description": "Price of the item",
                                    },
                                },
                                "required": ["name", "price"],
                            },
                        },
                        "tax_amount": {
                            "type": ["number", "null"],
                            "description": "Tax amount if available",
                        },
                        "payment_method": {
                            "type": ["string", "null"],
                            "description": "Payment method if available",
                        },
                    },
                    "required": [
                        "date",
                        "merchant_name",
                        "total_amount",
                        "items_purchased",
                    ],
                },
            }
        ]

    def add_receipt(self, receipt_data: Dict[str, Any], user_id: str) -> bool:
        """Add a receipt to the spreadsheet."""
        try:
            # Convert dictionary to Receipt model
            receipt = Receipt.from_dict(receipt_data)

            # Get user's credentials
            credentials = self.google_service.load_credentials(user_id)
            if not credentials:
                print("No valid credentials found for user")
                return False

            # Create new sheets service instance with credentials
            self.sheets_service = SheetsService()
            self.sheets_service.initialize(credentials)

            # Append receipt to spreadsheet
            self.sheets_service.append_receipt(receipt)

            return True
        except Exception as e:
            print(f"Error adding receipt to spreadsheet: {str(e)}")
            return False
