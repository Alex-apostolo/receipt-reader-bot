from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from telegram import Update
from app.config import WEBHOOK_URL
from app.telegram_bot import (
    telegram_app,
    initialize_bot,
    shutdown_bot,
)  # Import initialize and shutdown functions


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await telegram_app.bot.delete_webhook()
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    # Initialize the telegram application
    await initialize_bot()
    yield
    # Shutdown
    await shutdown_bot()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return {"status": "ok"}
