from telegram import Bot
from telegram.ext import Application
from app.config import TELEGRAM_TOKEN


class TelegramService:
    def __init__(self):
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.bot = self.app.bot

    async def initialize(self):
        """Initialize the bot application."""
        await self.app.initialize()

    async def shutdown(self):
        """Shutdown the bot application."""
        await self.app.shutdown()

    async def process_update(self, update):
        """Process an incoming update."""
        await self.app.process_update(update)

    def add_handler(self, handler):
        """Add a handler to the application."""
        self.app.add_handler(handler)
