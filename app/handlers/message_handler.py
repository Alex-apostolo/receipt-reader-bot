from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from app.services.google_service import GoogleService
from app.utils.create_auth_keyboard import create_auth_keyboard


class MessageHandler:
    def __init__(
        self,
        bot,
        google_service: GoogleService,
    ):
        self.bot = bot
        self.google_service = google_service

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages by informing users that the bot only handles photos."""
        await self.bot.send_message(
            chat_id=update.effective_chat.id,
            text="I can only process receipt photos! 📸\n\n"
            "Please send me a photo of your receipt, and I'll extract the information "
            "and save it to your Google Sheet.\n\n",
        )
