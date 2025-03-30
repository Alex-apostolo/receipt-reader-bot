from telegram import Update, Bot
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler as TelegramMessageHandler,
    CommandHandler as TelegramCommandHandler,
    filters,
)
from app.config import TELEGRAM_TOKEN
from app.google_auth import GoogleAuth
from app.handlers.command_handler import CommandHandler
from app.handlers.message_handler import MessageHandler
from app.handlers.oauth_handler import OAuthHandler


class TelegramBot:
    def __init__(self):
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.google_auth = GoogleAuth()
        self.bot = self.app.bot

        # Initialize handlers
        self.command_handler = CommandHandler(self.bot, self.google_auth)
        self.message_handler = MessageHandler(self.bot, self.google_auth)
        self.oauth_handler = OAuthHandler(self.bot, self.google_auth)

        self._register_handlers()

    def _register_handlers(self):
        """Register all command and message handlers."""
        # Command handlers
        self.app.add_handler(
            TelegramCommandHandler("start", self.command_handler.handle_start)
        )
        self.app.add_handler(
            TelegramCommandHandler("auth", self.command_handler.handle_auth)
        )
        self.app.add_handler(
            TelegramCommandHandler("logout", self.command_handler.handle_logout)
        )

        # Message handlers
        self.app.add_handler(
            TelegramMessageHandler(
                filters.TEXT & ~filters.COMMAND, self.message_handler.handle_text
            )
        )
        self.app.add_handler(
            TelegramMessageHandler(filters.PHOTO, self.message_handler.handle_photo)
        )

    async def handle_oauth_callback(self, code: str, state: str):
        """Handle the OAuth callback with the authorization code."""
        return await self.oauth_handler.handle_callback(code, state)

    async def initialize(self):
        """Initialize the bot application."""
        await self.app.initialize()

    async def shutdown(self):
        """Shutdown the bot application."""
        await self.app.shutdown()

    async def process_update(self, update: Update):
        """Process an incoming update."""
        await self.app.process_update(update)
