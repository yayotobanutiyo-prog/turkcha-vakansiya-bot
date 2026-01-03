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
OWNER_LINK = "https://t.me/Muhriddin_dev" # Sizning manzilingiz

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask('')
@app.route('/')
def home(): return "Bot ishlamoqda!"

def run(): app.run(host='0.0.0.0', port=8080)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user_text = update.message.text
    chat_type = update.message.chat.type

    # AI uchun yangilangan mukammal ko'rsatma (Prompt)
    prompt = f"""
    Sen "Turkcha Vakansiya Bot"san. Foydali, aqlli va sadoqatli yordamchisan.
    
    QOIDALARING:
    1. Yaratuvching (egang): Muhriddin (@Muhriddin_dev). Agar kimdir "Egang kim?", "Seni kim yaratgan?" deb so'rasa, g'urur bilan Muhriddin (@Muhriddin_dev) yaratganini ayt.
    2. Vakansiya saralash: Agar matn turkcha ish e'loni bo'lsa, uni O'zbek tiliga chiroyli qilib o'girib ber.
    3. Ish qidirish (Do'stlaring uchun): Agar foydalanuvchi o'z qobiliyatlarini yozsa (masalan: "Men haydovchiman", "Tikuvchilikni bilaman"), unga qanday ishlar mos kelishi haqida maslahat ber va motivatsiya ber.
    4. Suhbat: Oddiy salom-alik va savollarga do'stona javob ber.
    
    Foydalanuvchi yozuvi: {user_text}
    """
    
    try:
        response = model.generate_content(prompt)
        result = response.text
        
        if chat_type in ['group', 'supergroup']:
            # Guruhda faqat vakansiya bo'lsa egasiga yuboradi
            if any(word in user_text.lower() for word in ["iş", "eleman", "aranıyor", "vakansiya"]):
                await context.bot.send_message(chat_id=MY_CHAT_ID, text=f"Guruhdan yangi vakansiya:\n\n{result}")
        else:
            # Shaxsiyda hamma narsaga javob beradi
            await update.message.reply_text(result)
            
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    Thread(target=run).start()
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
