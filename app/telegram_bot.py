from telegram import Update, Bot
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)
from app.config import TELEGRAM_TOKEN
from app.llm_parser import extract_receipt_data


class TelegramBot:
    def __init__(self):
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self._register_handlers()

    def _register_handlers(self):
        """Register all command and message handlers."""
        self.app.add_handler(CommandHandler("start", self._start_command))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self._reply_working)
        )
        self.app.add_handler(MessageHandler(filters.PHOTO, self._handle_image))

    async def _start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        await update.message.reply_text(
            "Welcome to Receipt Reader Bot! 📸\n\n"
            "Send me a photo of your receipt, and I'll extract the information "
            "and save it to your Google Sheet."
        )

    async def _reply_working(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages."""
        await update.message.reply_text("Please send me a photo of your receipt 📸")

    async def _handle_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle receipt image uploads."""
        user_id = str(update.effective_user.id)
        photo = await update.message.photo[-1].get_file()

        # Get the file data as bytes
        file_data = await photo.download_as_bytearray()

        # Send directly to OpenAI
        await update.message.reply_text("Processing your receipt... 🔍")
        receipt_data = extract_receipt_data(file_data)

        # Clean up the response and send it back
        await update.message.reply_text(f"Receipt processed: {receipt_data}")

    async def initialize(self):
        """Initialize the bot application."""
        await self.app.initialize()

    async def shutdown(self):
        """Shutdown the bot application."""
        await self.app.shutdown()

    async def process_update(self, update: Update):
        """Process an incoming update."""
        await self.app.process_update(update)

    @property
    def bot(self) -> Bot:
        """Get the bot instance."""
        return self.app.bot
