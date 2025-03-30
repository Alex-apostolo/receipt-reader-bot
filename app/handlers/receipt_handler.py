from telegram import Update
from telegram.ext import ContextTypes
from app.services.google_service import GoogleService
from app.services.receipt_service import ReceiptService


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
            await self.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Please authenticate with Google first using the /auth command.",
            )
            return

        # Get the photo file
        photo = update.message.photo[-1]
        file = await self.bot.get_file(photo.file_id)

        try:
            # Download the photo as bytes
            file_data = await file.download_as_bytearray()

            # Process the receipt
            receipt_data = await self.receipt_service.process_receipt(file_data)

            # Initialize sheets service with user's credentials
            credentials = self.google_service.load_credentials(user_id)
            self.google_service.initialize_sheets_service(credentials)

            # Save to Google Sheets
            self.google_service.append_receipt(receipt_data)

            # Send success message
            await self.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Receipt processed and saved to your Google Sheet! ✅\n\n"
                f"Merchant: {receipt_data.get('merchant', 'N/A')}\n"
                f"Total: {receipt_data.get('total', 'N/A')}\n"
                f"Date: {receipt_data.get('date', 'N/A')}",
            )

        except Exception as e:
            print(f"Error processing receipt: {str(e)}")
            await self.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, there was an error processing your receipt. Please try again.",
            )
