import json
from telegram import Update
from telegram.ext import ContextTypes
from app.services.google_service import GoogleService
from app.services.receipt_service import ReceiptService
from app.utils.create_auth_keyboard import create_auth_keyboard


class ReceiptHandler:
    def __init__(
        self,
        bot,
        google_service: GoogleService,
        receipt_service: ReceiptService,
    ):
        self.bot = bot
        self.google_service = google_service
        self.receipt_service = receipt_service

    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle photo messages containing receipts."""
        user_id = str(update.effective_user.id)
        if not self.google_service.is_authenticated(user_id):
            reply_markup = create_auth_keyboard(user_id, self.google_service)
            await self.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Please connect your Google account first:",
                reply_markup=reply_markup,
            )
            return

        await self.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Processing receipt...",
        )
        # Get the photo file
        photo = update.message.photo[-1]
        file = await self.bot.get_file(photo.file_id)

        try:
            file_data = await file.download_as_bytearray()
            await self.receipt_service.process_receipt(file_data, user_id)

        except Exception as e:
            print(f"Error processing receipt: {str(e)}")
            await self.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, there was an error processing your receipt. Please try again.",
            )
