from telegram import Update
from telegram.ext import (
    MessageHandler as TelegramMessageHandler,
    CommandHandler as TelegramCommandHandler,
    filters,
)
from app.services.telegram_service import TelegramService
from app.services.google_service import GoogleService
from app.services.receipt_service import ReceiptService
from app.handlers.auth_handler import AuthHandler
from app.handlers.receipt_handler import ReceiptHandler
from app.handlers.message_handler import MessageHandler


class TelegramBot:
    def __init__(self):
        # Initialize services
        self.telegram_service = TelegramService()
        self.google_service = GoogleService()
        self.receipt_service = ReceiptService()

        # Initialize handlers
        self.auth_handler = AuthHandler(self.telegram_service.bot, self.google_service)
        self.receipt_handler = ReceiptHandler(
            self.telegram_service.bot, self.google_service, self.receipt_service
        )
        self.message_handler = MessageHandler(
            self.telegram_service.bot, self.google_service
        )

        self._register_handlers()

    def _register_handlers(self):
        """Register all command and message handlers."""
        # Command handlers
        self.telegram_service.add_handler(
            TelegramCommandHandler("start", self.message_handler.handle_text)
        )
        self.telegram_service.add_handler(
            TelegramCommandHandler("auth", self.auth_handler.handle_auth_command)
        )
        self.telegram_service.add_handler(
            TelegramCommandHandler("logout", self.auth_handler.handle_logout_command)
        )

        # Message handlers
        self.telegram_service.add_handler(
            TelegramMessageHandler(
                filters.TEXT & ~filters.COMMAND, self.message_handler.handle_text
            )
        )
        self.telegram_service.add_handler(
            TelegramMessageHandler(filters.PHOTO, self.receipt_handler.handle_photo)
        )

    async def handle_oauth_callback(self, code: str, state: str):
        """Handle the OAuth callback with the authorization code."""
        return await self.auth_handler.handle_oauth_callback(code, state)

    async def initialize(self):
        """Initialize the bot application."""
        await self.telegram_service.initialize()

    async def shutdown(self):
        """Shutdown the bot application."""
        await self.telegram_service.shutdown()

    async def process_update(self, update: Update):
        """Process an incoming update."""
        await self.telegram_service.process_update(update)

    @property
    def bot(self):
        return self.telegram_service.bot
