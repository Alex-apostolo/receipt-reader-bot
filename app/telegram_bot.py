from telegram import Update, Bot
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from app.config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)

# Create the bot app (like the dispatcher)
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()


# Add a simple text message handler
async def reply_working(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working ✅")


telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_working))


# Initialize the application
async def initialize_bot():
    await telegram_app.initialize()


# Cleanup function for graceful shutdown
async def shutdown_bot():
    await telegram_app.shutdown()
