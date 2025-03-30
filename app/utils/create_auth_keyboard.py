from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def create_auth_keyboard(self, user_id: str) -> InlineKeyboardMarkup:
    """Create an inline keyboard with the Google auth button."""
    auth_url = self.google_service.get_authorization_url(state=user_id)
    keyboard = [[InlineKeyboardButton("Connect Google Account", url=auth_url)]]
    return InlineKeyboardMarkup(keyboard)
