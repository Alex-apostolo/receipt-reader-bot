from telegram import Update, Bot
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from app.config import TELEGRAM_TOKEN
from app.llm_parser import extract_receipt_data

bot = Bot(token=TELEGRAM_TOKEN)

# Create the bot app (like the dispatcher)
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()


# Add a simple text message handler
async def reply_working(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working ✅")


telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_working))


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user
    photo = await update.message.photo[-1].get_file()

    # Get the file data as bytes
    file_data = await photo.download_as_bytearray()

    # Send directly to OpenAI
    receipt_data = extract_receipt_data(file_data)

    # Clean up the response and send it back
    await update.message.reply_text(f"Receipt processed: {receipt_data}")


telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_image))


# Initialize the application
async def initialize_bot():
    await telegram_app.initialize()


# Cleanup function for graceful shutdown
async def shutdown_bot():
    await telegram_app.shutdown()
