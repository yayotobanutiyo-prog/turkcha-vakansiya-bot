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

# Model nomini Google'ning eng so'nggi barqaror versiyasiga o'zgartirdik
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Render uchun kichik veb-server (Bot o'chib qolmasligi uchun)
app = Flask('')
@app.route('/')
def home(): return "Bot faol va ishlamoqda!"

def run(): app.run(host='0.0.0.0', port=8080)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    user_text = update.message.text
    chat_type = update.message.chat.type

    # AI uchun mukammal ko'rsatmalar to'plami
    prompt = f"""
    Sen "Turkcha Vakansiya Bot"san. Foydali, do'stona va sadoqatli yordamchisan.
    
    QOIDALAR:
    1. Yaratuvching (egang): Muhriddin (@Muhriddin_dev). Agar kimdir "Seni kim yasagan?", "Egang kim?", "Kimnikisan?" deb so'rasa, "Meni Muhriddin (@Muhriddin_dev) yaratgan" deb javob ber.
    2. Vakansiya saralash: Agar matn turkcha ish e'loni bo'lsa (ish, eleman, aranyor so'zlari bo'lsa), uni o'zbek tilida mana bu formatda sarala:
       📌 Lavozim:
       💰 Maosh:
       📍 Manzil:
       📞 Aloqa:
    3. Ish qidiruvchilarga yordam: Agar foydalanuvchi o'z hunarini aytsa (masalan: "Men tikuvchiman", "Haydovchilikni bilaman"), unga Turkiyada bunday ishlar qanday topilishi haqida maslahat va dalda ber.
    4. Suhbat: Oddiy "Salom", "Qalay" kabi gaplarga o'zbek tilida aqlli va samimiy javob ber.
    
    Foydalanuvchi yozdi: {user_text}
    """
    
    try:
        response = model.generate_content(prompt)
        result = response.text
        
        # Guruhlarda ish e'lonlarini saralab, sizga (egaga) yuboradi
        if chat_type in ['group', 'supergroup']:
            if any(word in user_text.lower() for word in ["iş", "eleman", "aranıyor", "vakansiya"]):
                await context.bot.send_message(chat_id=MY_CHAT_ID, text=f"Guruhdan yangi vakansiya topildi:\n\n{result}")
        else:
            # Shaxsiy suhbatda (lichkada) hamma narsaga javob qaytaradi
            await update.message.reply_text(result)
            
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    # Veb-serverni alohida oqimda ishga tushirish
    Thread(target=run).start()
    
    # Telegram botni ishga tushirish
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot ishga tushdi...")
    application.run_polling(drop_pending_updates=True) # "Conflict" xatosini kamaytirish uchun
