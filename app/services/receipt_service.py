import base64
from typing import Dict, Any
import os
import openai
from app.config import OPENAI_API_KEY


class ReceiptService:
    def __init__(self):
        self.temp_dir = "temp_receipts"
        os.makedirs(self.temp_dir, exist_ok=True)
        openai.api_key = OPENAI_API_KEY

    async def process_receipt(self, file_data: bytes) -> Dict[str, Any]:
        """Process receipt data and extract relevant information."""
        try:
            receipt_data = await self._extract_receipt_data(file_data)
            return receipt_data

        except Exception as e:
            print(f"Error processing receipt: {str(e)}")
            raise

    async def _extract_receipt_data(self, image_data: bytes) -> Dict[str, Any]:
        """Extract receipt data using OpenAI's GPT-4o."""
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
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract the following information from this receipt image: date, merchant name, total amount, items purchased, tax amount, and payment method. Format the response as a JSON object with these keys.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                },
                            },
                        ],
                    }
                ],
                response_format={"type": "json_object"},
                max_tokens=500,
            )

            # Parse the response and extract receipt data
            receipt_data = response.choices[0].message.content
            return receipt_data

        except Exception as e:
            print(f"Error extracting receipt data: {str(e)}")
            raise
