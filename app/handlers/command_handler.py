from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os
from app.services.google_service import GoogleService
from app.utils.create_auth_keyboard import create_auth_keyboard


class CommandHandler:
    def __init__(self, bot, google_service: GoogleService):
        self.bot = bot
        self.google_service = google_service

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        user_id = str(update.effective_user.id)
        if not self.google_service.is_authenticated(user_id):
            reply_markup = create_auth_keyboard(user_id, self.google_service)
            await update.message.reply_text(
                "Welcome to Receipt Reader Bot! 📸\n\n"
                "To get started, please connect your Google account first:",
                reply_markup=reply_markup,
            )
        else:
            await update.message.reply_text(
                "Welcome back to Receipt Reader Bot! 📸\n\n"
                "You're already connected to Google. Send me a photo of your receipt, "
                "and I'll extract the information and save it to your Google Sheet.\n\n"
                "Use /logout if you want to disconnect your Google account."
            )
