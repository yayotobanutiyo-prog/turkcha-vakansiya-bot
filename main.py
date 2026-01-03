import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# --- SOZLAMALAR ---
GEMINI_API_KEY = "AIzaSyCIjtFeGW7EN1ABt9COZ3KH48REWi2kASM"
TELEGRAM_BOT_TOKEN = "8284928912:AAFBHZlDJ20uK461iypQ8aROKg4w3zKS3QY"
MY_CHAT_ID = "594226936" 

# Model nomini eng so'nggi va barqaror versiyaga o'zgartirdik
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

app = Flask('')
@app.route('/')
def home(): return "Bot faol!"

def run(): app.run(host='0.0.0.0', port=8080)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user_text = update.message.text
    chat_type = update.message.chat.type

    prompt = f"""
    Sen "Turkcha Vakansiya Bot"san.
    QOIDALAR:
    1. Yaratuvching: Muhriddin (@Muhriddin_dev).
    2. Vakansiya: Turkcha ish e'lonlarini o'zbekcha sarala (Lavozim, Maosh, Manzil, Aloqa).
    3. Ish qidirish: Foydalanuvchi hunarini yozsa, unga mos ishlar haqida maslahat ber.
    4. Suhbat: Har qanday savolga o'zbek tilida aqlli va sadoqatli javob ber.
    Foydalanuvchi: {user_text}
    """
    
    try:
        response = model.generate_content(prompt)
        result = response.text
        if chat_type in ['group', 'supergroup']:
            if any(word in user_text.lower() for word in ["iş", "eleman", "aranıyor", "vakansiya"]):
                await context.bot.send_message(chat_id=MY_CHAT_ID, text=f"Guruhdan vakansiya:\n\n{result}")
        else:
            await update.message.reply_text(result)
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    Thread(target=run).start()
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot ishga tushdi...")
    # drop_pending_updates=True eski "Conflict" xabarlarini tozalaydi
    application.run_polling(drop_pending_updates=True)

