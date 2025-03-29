from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram import Update
from app.config import WEBHOOK_URL
from app.telegram_bot import TelegramBot


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


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_bot.bot)
    await telegram_bot.process_update(update)
    return {"status": "ok"}
