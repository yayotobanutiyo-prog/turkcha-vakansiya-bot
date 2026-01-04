import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# --- SOZLAMALAR ---
# Google AI API kaliti
GEMINI_API_KEY = "AIzaSyCIjtFeGW7EN1ABt9COZ3KH48REWi2kASM"
# Siz hozirgina ochgan yangi bot tokeni
TELEGRAM_BOT_TOKEN = "8240634759:AAHuD-4x4yAZ9o2IQKdJU9B26d9Dxl_Icd0"
# Sizning chat ID (vakansiyalarni saralash uchun)
MY_CHAT_ID = "594226936" 

# Gemini AI modelini sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Render serveri uchun kichik veb-interfeys (Bot o'chib qolmasligi uchun)
app = Flask('')
@app.route('/')
def home(): return "Yangi bot muvaffaqiyatli ishlamoqda!"

def run(): app.run(host='0.0.0.0', port=8080)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user_text = update.message.text
    chat_type = update.message.chat.type

    # AI uchun yo'riqnoma
    prompt = f"""
    Sen "Turkcha Vakansiya Bot"san. Muhriddin (@Muhriddin_dev) tomonidan yaratilgan aqlli yordamchisan.
    
    VAZIFALARING:
    1. Agar foydalanuvchi turkcha ish e'loni yuborsa (ish, eleman, aranyor kabi so'zlar bo'lsa), uni o'zbek tilida: Lavozim, Maosh, Manzil va Aloqa qilib chiroyli sarala.
    2. Agar foydalanuvchi "Seni kim yaratgan?" deb so'rasa, "Meni Muhriddin (@Muhriddin_dev) yaratgan" deb javob ber.
    3. Boshqa barcha savollarga o'zbek tilida muloyim va aqlli javob qaytar.
    
    Foydalanuvchi yozdi: {user_text}
    """
    
    try:
        response = model.generate_content(prompt)
        result = response.text
        
        if chat_type in ['group', 'supergroup']:
            # Guruhlarda faqat vakansiya bo'lsa Muhriddinga yuboradi
            if any(word in user_text.lower() for word in ["iş", "eleman", "aranıyor", "vakansiya"]):
                await context.bot.send_message(chat_id=MY_CHAT_ID, text=f"Guruhdan vakansiya keldi:\n\n{result}")
        else:
            # Shaxsiy suhbatda har doim javob beradi
            await update.message.reply_text(result)
            
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    # Veb-serverni ishga tushirish
    Thread(target=run).start()
    
    # Telegram botni ishga tushirish
    # drop_pending_updates=True eski xabarlarni tozalab, botni toza ishga tushiradi
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Yangi bot ishga tushdi...")
    application.run_polling(drop_pending_updates=True)

