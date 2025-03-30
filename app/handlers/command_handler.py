from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import os
from .base_handler import BaseHandler


class CommandHandler(BaseHandler):
    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        user_id = self._get_user_id(update)

        if not self.google_auth.is_authenticated(user_id):
            reply_markup = self._create_auth_keyboard(user_id)
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

    async def handle_auth(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /auth command to start Google OAuth flow."""
        user_id = self._get_user_id(update)

        if self.google_auth.is_authenticated(user_id):
            await update.message.reply_text(
                "You are already authenticated with Google! ✅\n"
                "Your receipts will be saved to your Google Sheet."
            )
            return

        reply_markup = self._create_auth_keyboard(user_id)
        await update.message.reply_text(
            "Please connect your Google account to save receipts to your Google Sheet:",
            reply_markup=reply_markup,
        )

    async def handle_logout(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /logout command to revoke Google access."""
        user_id = self._get_user_id(update)

        if not self.google_auth.is_authenticated(user_id):
            await update.message.reply_text(
                "You are not currently connected to Google. Use /auth to connect your account."
            )
            return

        # Remove credentials file
        creds_path = os.path.join("user_credentials", f"{user_id}_google_creds.json")
        if os.path.exists(creds_path):
            os.remove(creds_path)
            await update.message.reply_text(
                "Successfully disconnected from Google! ✅\n"
                "Use /auth to connect again when you want to save receipts to your Google Sheet."
            )
        else:
            await update.message.reply_text(
                "You are not currently connected to Google. Use /auth to connect your account."
            )
