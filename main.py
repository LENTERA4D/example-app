import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from fastapi import FastAPI
from dotenv import load_dotenv

# Load ENV (local only, on Railway pakai Dashboard)
load_dotenv()
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError("TOKEN environment variable not set!")

# FastAPI app (untuk nge-ping di Railway)
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "✅ Lentera4D Telegram Bot is running on Railway."}

# Gambar banner
BANNER_URL = "https://i.postimg.cc/zfYykbf1/button-travel-lifestyle-hijau.png"

# Handler untuk /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        return

    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type

    # 1. Kirim gambar banner
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=BANNER_URL,
        caption=(
            "🎰 Selamat Datang di Lentera4D 🎰\n"
            "Kami ucapkan terima kasih telah bergabung bersama kami.\n"
            "Semoga Anda mendapatkan pengalaman bermain terbaik, aman, dan menguntungkan 🤩\n"
            "Jika ada pertanyaan, tim kami siap membantu 24 jam penuh 🥰"
        )
    )

    # 2. Kirim tombol menu
    keyboard = [
        [InlineKeyboardButton("⚡ LINK ALTERNATIVE ⚡", url="https://heylink.me/LENTERA4D.VIP/")],
        [InlineKeyboardButton("🎰 RTP SLOT", url="https://lentera4dprediksijp.vip/rtp/")],
        [InlineKeyboardButton("💬 LIVE CHAT LENTERA4D 💬", url="https://tawk.to/chat/617b8ef5f7c0440a59208637/1fj5acrtg")],
        [InlineKeyboardButton("📘 FACEBOOK GRUB", url="https://t.ly/FB-LT"),
         InlineKeyboardButton("🏦 TUTOR QRIS", url="https://cara-deposit-qris.site/lentera4d/")],
        [InlineKeyboardButton("📱 WHATSAPP LENTERA4D", url="https://wa.me/6285947212195"),
         InlineKeyboardButton("📊 PREDIKSI TOGEL", url="https://t.ly/prediksi-lentera4d")],
        [InlineKeyboardButton("📲 TELEGRAM LENTERA4D", url="https://t.me/admlentera4d")],
        [InlineKeyboardButton("🔐 LOGIN LENTERA4D", url="https://lentera4d1103.top/?content=register&ref=bakayaro")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="👇 Klik salah satu menu:", reply_markup=reply_markup)

    # 3. Jika chat di grup, kirim jumlah member
    if chat_type in ['group', 'supergroup']:
        member_count = await context.bot.get_chat_member_count(chat_id)
        await context.bot.send_message(chat_id=chat_id, text=f"👥 Jumlah Member Grup Saat Ini: {member_count} orang")

# Jalankan Telegram bot saat FastAPI startup
@app.on_event("startup")
async def startup():
    telegram_app = ApplicationBuilder().token(TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    print("✅ Bot aktif dan siap menerima perintah...")
    telegram_app.run_polling()
