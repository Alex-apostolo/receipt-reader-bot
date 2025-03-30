from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.services.google_service import GoogleService


def create_auth_keyboard(
    user_id: str, google_service: GoogleService
) -> InlineKeyboardMarkup:
    """Create an inline keyboard with the Google auth button."""
    auth_url = google_service.get_authorization_url(state=user_id)
    keyboard = [[InlineKeyboardButton("Connect Google Account", url=auth_url)]]
    return InlineKeyboardMarkup(keyboard)
