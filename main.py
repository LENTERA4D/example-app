import os
from fastapi import FastAPI
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from app.handlers import start

# Load ENV (only works locally, Railway uses Dashboard ENV)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Bot is running on Railway!"}

# Init Telegram bot (run this only once)
@app.on_event("startup")
async def startup():
    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.run_polling()
