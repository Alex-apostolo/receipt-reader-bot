from telegram import Update
from telegram.ext import ContextTypes
from app.services.google_service import GoogleService
from app.utils.create_auth_keyboard import create_auth_keyboard


class AuthHandler:
    def __init__(self, bot, google_service: GoogleService):
        self.bot = bot
        self.google_service = google_service

    async def handle_auth_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle the /auth command to start Google OAuth flow."""
        user_id = str(update.effective_user.id)
        if self.google_service.is_authenticated(user_id):
            await update.message.reply_text(
                "You are already authenticated with Google! ✅\n"
                "Your receipts will be saved to your Google Sheet."
            )
            return

        reply_markup = create_auth_keyboard(user_id)
        await update.message.reply_text(
            "Please connect your Google account to save receipts to your Google Sheet:",
            reply_markup=reply_markup,
        )

    async def handle_logout_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handle the /logout command to revoke Google access."""
        user_id = str(update.effective_user.id)
        if not self.google_service.is_authenticated(user_id):
            await update.message.reply_text(
                "You are not currently connected to Google."
            )
            return

        if self.google_service.revoke_access(user_id):
            await update.message.reply_text(
                "Successfully disconnected from Google! ✅\n"
                "Use /auth to connect again when you want to save receipts to your Google Sheet."
            )
        else:
            await update.message.reply_text(
                "You are not currently connected to Google."
            )

    async def handle_oauth_callback(self, code: str, state: str) -> bool:
        """Handle the OAuth callback with the authorization code."""
        try:
            credentials = self.google_service.get_credentials_from_code(code)
            self.google_service.save_credentials(credentials, state)
            # Send success message to user
            await self.bot.send_message(
                chat_id=state,
                text="Successfully authenticated with Google! ✅\n"
                "Now you can send me photos of your receipts, and I'll save them to your Google Sheet.",
            )
            return True
        except Exception as e:
            print(f"OAuth callback error: {str(e)}")
            # Send error message to user
            await self.bot.send_message(
                chat_id=state,
                text="❌ Authentication failed. Please try connecting your Google account again.",
            )
            return False
