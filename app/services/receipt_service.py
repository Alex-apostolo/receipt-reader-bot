import base64
import json
from typing import Dict, Any, Optional, Tuple
import os
import openai
from app.config import OPENAI_API_KEY
from app.models.receipt import Receipt
from app.tools.spreadsheet_tool import SpreadsheetTool
from app.services.google_service import GoogleService
from app.agents.receipt_agent import ReceiptAgent


class ReceiptService:
    def __init__(self, google_service: GoogleService):
        self.temp_dir = "temp_receipts"
        os.makedirs(self.temp_dir, exist_ok=True)
        openai.api_key = OPENAI_API_KEY
        self.spreadsheet_tool = SpreadsheetTool(google_service)
        self.agent = ReceiptAgent(google_service)

    async def process_receipt(
        self, image_data: bytes, user_id: str
    ) -> Optional[Tuple[str]]:
        """Process receipt data and extract relevant information."""
        return await self.agent.process_receipt(image_data, user_id)
