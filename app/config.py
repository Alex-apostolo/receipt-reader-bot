import os
from dotenv import load_dotenv

load_dotenv(override=True)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Google Sheets Configuration
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID_HERE"  # Replace with your actual spreadsheet ID
