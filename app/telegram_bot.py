from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler as TelegramMessageHandler,
    CommandHandler as TelegramCommandHandler,
    filters,
)
from app.config import TELEGRAM_TOKEN
from app.handlers.command_handler import CommandHandler
from app.services.google_service import GoogleService
from app.services.receipt_service import ReceiptService
from app.handlers.auth_handler import AuthHandler
from app.handlers.receipt_handler import ReceiptHandler
from app.handlers.message_handler import MessageHandler
from app.services.sheets_service import SheetsService


class TelegramBot:
    def __init__(self):
        # Initialize application
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.bot = self.app.bot

        # Initialize services
        self.google_service = GoogleService()
        self.receipt_service = ReceiptService()
        self.sheets_service = SheetsService()

        # Initialize handlers
        self.auth_handler = AuthHandler(self.bot, self.google_service)
        self.receipt_handler = ReceiptHandler(
            self.bot, self.google_service, self.receipt_service, self.sheets_service
        )
        self.message_handler = MessageHandler(self.bot, self.google_service)
        self.command_handler = CommandHandler(self.bot, self.google_service)

        self._register_handlers()

    def _register_handlers(self):
        """Register all command and message handlers."""
        # Command handlers
        self.app.add_handler(
            TelegramCommandHandler("start", self.command_handler.handle_start)
        )
        self.app.add_handler(
            TelegramCommandHandler("logout", self.auth_handler.handle_logout_command)
        )

        # Message handlers
        self.app.add_handler(
            TelegramMessageHandler(
                filters.TEXT & ~filters.COMMAND, self.message_handler.handle_text
            )
        )
        self.app.add_handler(
            TelegramMessageHandler(filters.PHOTO, self.receipt_handler.handle_photo)
        )

    async def handle_oauth_callback(self, code: str, state: str):
        """Handle the OAuth callback with the authorization code."""
        return await self.auth_handler.handle_oauth_callback(code, state)

    async def initialize(self):
        """Initialize the bot application."""
        await self.app.initialize()

    async def shutdown(self):
        """Shutdown the bot application."""
        await self.app.shutdown()

    async def process_update(self, update: Update):
        """Process an incoming update."""
        await self.app.process_update(update)
