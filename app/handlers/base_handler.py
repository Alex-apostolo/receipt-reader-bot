from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from app.google_auth import GoogleAuth


class BaseHandler:
    def __init__(self, bot: Bot, google_auth: GoogleAuth):
        self.bot = bot
        self.google_auth = google_auth

    def _get_user_id(self, update: Update) -> str:
        """Get the user ID from an update."""
        return str(update.effective_user.id)

    def _create_auth_keyboard(self, user_id: str) -> InlineKeyboardMarkup:
        """Create an authentication keyboard with the auth URL."""
        auth_url = self.google_auth.get_authorization_url(state=user_id)
        keyboard = [[InlineKeyboardButton("Connect Google Account", url=auth_url)]]
        return InlineKeyboardMarkup(keyboard)

    async def _check_auth(self, update: Update) -> bool:
        """Check if user is authenticated and show auth button if not."""
        user_id = self._get_user_id(update)
        if not self.google_auth.is_authenticated(user_id):
            reply_markup = self._create_auth_keyboard(user_id)
            await update.message.reply_text(
                "Please connect your Google account first to use this bot:",
                reply_markup=reply_markup,
            )
            return False
        return True
