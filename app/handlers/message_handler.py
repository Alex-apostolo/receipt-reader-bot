from telegram import Update
from telegram.ext import ContextTypes
from app.llm_parser import extract_receipt_data
from .base_handler import BaseHandler


class MessageHandler(BaseHandler):
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages."""
        if not await self._check_auth(update):
            return
        await update.message.reply_text("Please send me a photo of your receipt 📸")

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle receipt image uploads."""
        if not await self._check_auth(update):
            return

        photo = await update.message.photo[-1].get_file()
        file_data = await photo.download_as_bytearray()
        await self._process_image_data(self._get_user_id(update), file_data)

    async def _process_image_data(self, user_id: str, file_data: bytes):
        """Process image data and extract receipt information."""
        # Send processing message
        await self.bot.send_message(
            chat_id=user_id, text="Processing your receipt... 🔍"
        )

        # Extract receipt data
        receipt_data = extract_receipt_data(file_data)

        # Send the result
        await self.bot.send_message(
            chat_id=user_id, text=f"Receipt processed: {receipt_data}"
        )
