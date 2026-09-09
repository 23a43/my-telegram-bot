import os
import asyncio
import requests
from telegram import Update
# ✅ সঠিক লাইন:
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
TELEGRAM_BOT_TOKEN = "8813169317:AAFfxhHRSxaMT29FYYvMfNXHuSJty1eQTNY"
GEMINI_API_KEY = "AQ.Ab8RN6Jsg1iK7VLUDoBlOA9pVXDWidY3_N1Xn51Y3mGrpzr3Tw"

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

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot starting...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
