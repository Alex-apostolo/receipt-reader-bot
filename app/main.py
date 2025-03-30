from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram import Update
from app.config import WEBHOOK_URL
from app.telegram_bot import TelegramBot
from fastapi.responses import RedirectResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await telegram_bot.bot.delete_webhook()
    await telegram_bot.bot.set_webhook(url=WEBHOOK_URL)
    # Initialize the telegram application
    await telegram_bot.initialize()
    yield
    # Shutdown
    await telegram_bot.shutdown()


app = FastAPI(lifespan=lifespan)
telegram_bot = TelegramBot()


@app.get("/webhook")
async def oauth_callback(code: str, state: str):
    """Handle Google OAuth callback."""
    await telegram_bot.handle_oauth_callback(code, state)
    # Redirect back to Telegram
    return RedirectResponse(url="https://t.me/receipt_reader_42_bot")


@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Handle Telegram updates."""
    data = await request.json()
    update = Update.de_json(data, telegram_bot.bot)
    await telegram_bot.process_update(update)
    return {"status": "ok"}
