import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# --- SOZLAMALAR ---
GEMINI_API_KEY = "AIzaSyCIjtFeGW7EN1ABt9COZ3KH48REWi2kASM"
# Siz hozirgina REVOKE qilib olgan eng yangi tokeningiz
TELEGRAM_BOT_TOKEN = "8240634759:AAHC7hdGF6E_erK_zoKmSxyolvKaqnBrg8c"
MY_CHAT_ID = "594226936" 

# Gemini AI modelini sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Render serveri uchun veb-interfeys
app = Flask('')
@app.route('/')
def home(): return "Bot uyg'ondi va ishlamoqda!"

def run(): app.run(host='0.0.0.0', port=8080)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user_text = update.message.text
    chat_type = update.message.chat.type

    # AI yo'riqnomasi
    prompt = f"Sen 'Turkcha Vakansiya Bot'san. Muhriddin (@Muhriddin_dev) yaratgan yordamchisan. Savolga o'zbekcha javob ber: {user_text}"
    
    try:
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Xatolik: {e}")

if __name__ == '__main__':
    Thread(target=run).start()
    
    # drop_pending_updates=True eski tiqilib qolgan xabarlarni o'chirib yuboradi
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Yangi bot ishga tushdi...")
    application.run_polling(drop_pending_updates=True)

