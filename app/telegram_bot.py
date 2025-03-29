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

# Create the bot app (like the dispatcher)
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()


# Command handler for /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Receipt Reader Bot! 📸\n\n"
        "Send me a photo of your receipt, and I'll extract the information "
        "and save it to your Google Sheet."
    )


# Add a simple text message handler
async def reply_working(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please send me a photo of your receipt 📸")


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    photo = await update.message.photo[-1].get_file()

    # Get the file data as bytes
    file_data = await photo.download_as_bytearray()

    # Send directly to OpenAI
    await update.message.reply_text("Processing your receipt... 🔍")
    receipt_data = extract_receipt_data(file_data)

    # Clean up the response and send it back
    await update.message.reply_text(f"Receipt processed: {receipt_data}")


# Initialize the application
async def initialize_bot():
    await telegram_app.initialize()


# Cleanup function for graceful shutdown
async def shutdown_bot():
    await telegram_app.shutdown()


# Register handlers
telegram_app.add_handler(CommandHandler("start", start_command))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_working))
telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_image))
