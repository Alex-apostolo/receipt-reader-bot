from telegram import Update
from telegram.ext import ContextTypes
from app.services.google_service import GoogleService
from app.services.receipt_service import ReceiptService
from app.utils.create_auth_keyboard import create_auth_keyboard


class MessageHandler:
    def __init__(
        self,
        bot,
        google_service: GoogleService,
        receipt_service: ReceiptService,
    ):
        self.bot = bot
        self.google_service = google_service
        self.receipt_service = receipt_service

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages."""
        user_id = str(update.effective_user.id)
        if not self.google_service.is_authenticated(user_id):
            reply_markup = create_auth_keyboard(user_id)
            await self.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Please authenticate with Google first using the button below.",
                reply_markup=reply_markup,
            )
            return

        await self.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please send me a photo of your receipt.",
        )
