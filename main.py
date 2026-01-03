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

# Model nomini 'gemini-pro'ga o'zgartirdik, bu eng ishonchli va 404 xatosi bermaydigan versiya
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Render serveri uchun kichik veb-interfeys
app = Flask('')
@app.route('/')
def home(): return "Bot faol va ishlamoqda!"

def run(): app.run(host='0.0.0.0', port=8080)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user_text = update.message.text
    chat_type = update.message.chat.type

    # AI uchun yangilangan yo'riqnoma
    prompt = f"""
    Sen "Turkcha Vakansiya Bot"san. Foydali va sadoqatli yordamchisan.
    
    QOIDALAR:
    1. Yaratuvching: Muhriddin (@Muhriddin_dev). Agar kimdir seni kim yaratganini so'rasa, "Meni Muhriddin (@Muhriddin_dev) yaratgan" deb javob ber.
    2. Vakansiya saralash: Agar matn turkcha ish e'loni bo'lsa (ish, eleman, aranyor so'zlari bo'lsa), uni o'zbek tilida: Lavozim, Maosh, Manzil va Aloqa formatida sarala.
    3. Ish qidiruvchilarga: Ularning hunariga qarab Turkiyadan ish topish bo'yicha maslahat ber.
    4. Suhbat: Har qanday savolga o'zbek tilida aqlli javob ber.
    
    Foydalanuvchi yozdi: {user_text}
    """
    
    try:
        response = model.generate_content(prompt)
        result = response.text
        
        if chat_type in ['group', 'supergroup']:
            # Guruhlarda faqat vakansiya so'zlari bo'lsa sizga yuboradi
            if any(word in user_text.lower() for word in ["iş", "eleman", "aranıyor", "vakansiya"]):
                await context.bot.send_message(chat_id=MY_CHAT_ID, text=f"Guruhdan yangi vakansiya:\n\n{result}")
        else:
            # Shaxsiy suhbatda har doim javob qaytaradi
            await update.message.reply_text(result)
            
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    # Veb-serverni ishga tushirish
    Thread(target=run).start()
    
    # Telegram botni ishga tushirish
    # drop_pending_updates=True - bu eski tiqilib qolgan xabarlarni tozalaydi
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot ishga tushdi...")
    application.run_polling(drop_pending_updates=True)

