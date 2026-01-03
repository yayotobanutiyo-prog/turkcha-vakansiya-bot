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

# Gemini AI ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Render o‘chib qolmasligi uchun kichik Web Server (Flask)
app = Flask('')
@app.route('/')
def home():
    return "Bot yoniq va ishlamoqda!"

def run():
    app.run(host='0.0.0.0', port=8080)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Xabar matni borligini tekshirish
    if not update.message or not update.message.text:
        return
    
    text = update.message.text
    
    # AI ga vazifa (Prompt)
    prompt = f"""
    Ushbu turkcha matnni tahlil qil. 
    Agar bu ish e'loni (vakansiya) bo'lsa, uni quyidagi formatda o'zbek tilida saralab ber:
    
    📌 **Lavozim:** (ish nomi)
    💰 **Maosh:** (ko'rsatilgan bo'lsa)
    📍 **Manzil:** (shahar yoki hudud)
    📞 **Aloqa:** (telefon yoki telegram link)
    
    Agar matn ish e'loni bo'lmasa, faqat bitta 'NO' so'zini qaytar.
    Matn: {text}
    """
    
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        
        # Agar AI vakansiya deb topsa, sizga yuboradi
        if "NO" not in result.upper():
            await context.bot.send_message(
                chat_id=MY_CHAT_ID, 
                text=f"Yangi Vakansiya Topildi! 🔥\n\n{result}",
                parse_mode='Markdown'
            )
    except Exception as e:
        print(f"Xato yuz berdi: {e}")

if __name__ == '__main__':
    # Web serverni alohida oqimda ishga tushirish
    Thread(target=run).start()
    
    # Telegram botni sozlash va ishga tushirish
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot muvaffaqiyatli ishga tushdi!")
    application.run_polling()
