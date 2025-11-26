import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====== SOZLAMALAR ======
TELEGRAM_TOKEN = "8369388611:AAEqKYEcLC5cQsLfbjXA-JYEgGXETjk34aA"
GROQ_API_KEY = "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"

# Groq clientini sozlash
groq_client = Groq(api_key=GROQ_API_KEY)

# Tibbiy bot uchun system prompt
SYSTEM_PROMPT = """Sen professional tibbiy maslahatchi botsan. O'zbekcha javob berasan.

MUHIM QOIDALAR:
1. Agar kasallik yengil bo'lsa (shamollash, yengil bosh og'rig'i) - uy davolash usullarini ayt
2. Agar alomatlar jiddiy bo'lsa (yuqori harorat 3 kundan ko'p, kuchli og'riq, qon ketishi) - ALBATTA shifokorga murojaat qilishni yoki 103 ga qo'ng'iroq qilishni ayt
3. Har doim ehtiyotkor bo'l va zarur hollarda professional yordam olishni tavsiya qil
4. Javoblaringni qisqa va tushunarli qil
5. Hech qachon aniq tashxis qo'yma, faqat umumiy maslahat ber

O'zbekcha yoz va oddiy tilda tushuntir."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot boshlanganda chiqadigan xabar"""
    logger.info(f"User {update.effective_user.id} started the bot")
    
    welcome_text = """🏥 Assalomu alaykum! Men tibbiy maslahat botiman.

Men sizga quyidagicha yordam bera olaman:
✅ Kasallik alomatlari haqida ma'lumot
✅ Uy davolash usullari
✅ Qachon shifokorga borish kerakligini aytish

⚠️ MUHIM: Men haqiqiy shifokor emasman! Jiddiy holatlarda albatta shifokorga murojaat qiling.

Menga kasallik yoki alomatlaringizni yozing, men yordam beraman! 😊"""
    
    await update.message.reply_text(welcome_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi xabarini qayta ishlash"""
    user_message = update.message.text
    user_id = update.effective_user.id
    
    logger.info(f"Received message from {user_id}: {user_message}")
    
    # "Yozmoqda..." ko'rsatish
    await update.message.chat.send_action("typing")
    
    try:
        # Groq AI'ga so'rov yuborish
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1000
        )
        
        # Javobni olish
        ai_response = chat_completion.choices[0].message.content
        logger.info(f"AI response generated for {user_id}")
        
        # Javobni yuborish
        await update.message.reply_text(ai_response)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        error_message = f"❌ Xatolik yuz berdi: {str(e)}\n\nIltimos, qaytadan urinib ko'ring."
        await update.message.reply_text(error_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam buyrug'i"""
    help_text = """📚 Qanday foydalanish:

1️⃣ Menga kasallik yoki alomatlaringizni yozing
   Masalan: "Boshim og'riyapti va haroratim bor"

2️⃣ Men sizga maslahat beraman:
   • Yengil kasallik - uy davolash
   • Jiddiy holat - shifokor/103

⚠️ Eslatma: Men haqiqiy shifokor emasman!

Savollaringizni bemalol yozing! 😊"""
    
    await update.message.reply_text(help_text)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xatolarni qayta ishlash"""
    logger.error(f"Update {update} caused error {context.error}")


def main():
    """Botni ishga tushirish"""
    print("\n" + "="*50)
    print("🤖 TIBBIY MASLAHAT BOT")
    print("="*50)
    print("📱 Bot ishga tushmoqda...")
    print("⏳ Iltimos, kuting...\n")
    
    try:
        # Application yaratish
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Handlerlarni qo'shish
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        # Botni ishga tushirish
        print("✅ Bot muvaffaqiyatli ishga tushdi!")
        print("📞 Telegram'da botingizni toping va /start buyrug'ini yuboring")
        print("🛑 To'xtatish uchun Ctrl+C bosing\n")
        print("="*50 + "\n")
        
        # Polling
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        
    except Exception as e:
        print(f"\n❌ XATOLIK: {e}")
        print("\nTekshiring:")
        print("  1. Internet ulanishi")
        print("  2. Token to'g'riligi")
        print("  3. Groq API key faolligi\n")


if __name__ == "__main__":
    main()