import base64
import json
from typing import Dict, Any, Optional, Tuple
import openai
from app.config import OPENAI_API_KEY
from app.models.receipt import Receipt
from app.tools.spreadsheet_tool import SpreadsheetTool
from app.services.google_service import GoogleService


class ReceiptAgent:
    def __init__(self, google_service: GoogleService):
        openai.api_key = OPENAI_API_KEY
        self.spreadsheet_tool = SpreadsheetTool(google_service)
        self.messages = [
            {
                "role": "system",
                "content": """You are a receipt processing agent. Your task is to:
                1. Extract information from receipt images
                2. Format the data according to the specified schema
                3. Save the data using the provided function
                
                Always verify the extracted data before saving.
                If you're unsure about any information, mark it as null or use your best judgment.
                """,
            }
        ]

    async def process_receipt(
        self, image_data: bytes, user_id: str
    ) -> Tuple[Optional[str]]:
        """Process a receipt image and save the data."""
        try:
            # Convert image data to base64
            if isinstance(image_data, (bytes, bytearray)):
                image_data = base64.b64encode(image_data).decode("utf-8")

            # Add user message with image
            self.messages.append(
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
                }
            )

            # Get response from OpenAI
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=self.messages,
                functions=self.spreadsheet_tool.function_schema,
                function_call={"name": "add_receipt"},
                max_tokens=500,
            )

            # Process the response
            message = response.choices[0].message
            self.messages.append(message)

            # Handle function call
            if message.function_call and message.function_call.name == "add_receipt":
                receipt_data = json.loads(message.function_call.arguments)

                # Save to spreadsheet
                if self.spreadsheet_tool.add_receipt(receipt_data, user_id):
                    # Add function result to messages
                    self.messages.append(
                        {
                            "role": "function",
                            "name": "add_receipt",
                            "content": json.dumps({"success": True}),
                        }
                    )
                    spreadsheetUrl = (
                        self.spreadsheet_tool.sheets_service.get_spreadsheet_url()
                    )
                    return spreadsheetUrl
                else:
                    # Add error to messages
                    self.messages.append(
                        {
                            "role": "function",
                            "name": "add_receipt",
                            "content": json.dumps(
                                {"success": False, "error": "Failed to save receipt"}
                            ),
                        }
                    )
                    return None
            else:
                raise ValueError("No valid function call in response")

        except Exception as e:
            print(f"Error processing receipt: {str(e)}")
            # Add error to messages
            self.messages.append(
                {"role": "assistant", "content": f"Error processing receipt: {str(e)}"}
            )
            return None
