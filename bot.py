import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== CONFIGURATION ====================
# ১. Telegram Bot Token (BotFather থেকে নেওয়া)
TELEGRAM_BOT_TOKEN = "8844521108:AAGFgoupE4cRiTS7nvDujNUt5N0d1K8FZ6Q"

# ২. Google Gemini API Key (Google AI Studio থেকে নেওয়া)
GEMINI_API_KEY = "AQ.Ab8RN6Jsg1iK7VLUDoBlOA9pVXDWidY3_N1Xn51Y3mGrpzr3Tw"
# =======================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমি আপনার AI Job Agent। আমাকে যেকোনো প্রশ্ন করতে পারেন।")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.chat.send_action(action="typing")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": user_text}]}]}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        if response.status_code == 200 and "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            reply = "দুঃখিত, কোনো সমস্যা হয়েছে।"
    except Exception:
        reply = "Gemini API-তে সংযোগ করতে সমস্যা হচ্ছে।"

    await update.message.reply_text(reply)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
