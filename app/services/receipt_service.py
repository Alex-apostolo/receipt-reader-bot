import base64
import json
from typing import Dict, Any
import os
import openai
from app.config import OPENAI_API_KEY
from app.models.receipt import Receipt
from app.tools.spreadsheet_tool import SpreadsheetTool
from app.services.google_service import GoogleService


class ReceiptService:
    def __init__(self, google_service: GoogleService):
        self.temp_dir = "temp_receipts"
        os.makedirs(self.temp_dir, exist_ok=True)
        openai.api_key = OPENAI_API_KEY
        self.spreadsheet_tool = SpreadsheetTool(google_service)

    async def process_receipt(self, image_data: bytes, user_id: str) -> Receipt:
        """Process receipt data and extract relevant information."""
        try:
            # If the input is a file path (string), read it
            if isinstance(image_data, str):
                with open(image_data, "rb") as file:
                    image_data = file.read()

            # Convert image data to base64
            if isinstance(image_data, (bytes, bytearray)):
                image_data = base64.b64encode(image_data).decode("utf-8")

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a receipt processing assistant. Extract information from receipt images and save them using the provided function.",
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract the following information from this receipt image: date, merchant name, total amount, items purchased (with prices), tax amount, and payment method. Use the add_receipt function to save the data.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                },
                            },
                        ],
                    },
                ],
                functions=self.spreadsheet_tool.function_schema,
                function_call={"name": "add_receipt"},
                max_tokens=500,
            )

            # Get the function call arguments
            function_call = response.choices[0].message.function_call
            if function_call and function_call.name == "add_receipt":
                receipt_data = json.loads(function_call.arguments)
                print("RECEIPT DATA", receipt_data)

                # Save to spreadsheet using the tool
                if self.spreadsheet_tool and user_id:
                    self.spreadsheet_tool.add_receipt(receipt_data, user_id)

                return Receipt.from_dict(receipt_data)
            else:
                raise ValueError("No valid function call in response")

        except Exception as e:
            print(f"Error processing receipt: {str(e)}")
            raise
