
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Groq client import va sozlash (to‘g‘ri versiya)
from groq import Client
groq_client = Client(api_key="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")

# Logging sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====== SOZLAMALAR ======
TELEGRAM_TOKEN = "8369388611:AAEqKYEcLC5cQsLfbjXA-JYEgGXETjk34aA"

SYSTEM_PROMPT = """Sen professional tibbiy maslahatchi botsan. O'zbekcha javob berasan."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏥 Assalomu alaykum! Men tibbiy maslahat botiman. Menga alomatlaringizni yozing 😊")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.chat.send_action("typing")

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=500
        )

        ai_reply = completion.choices[0].message.content
        await update.message.reply_text(ai_reply)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}\nQaytadan urinib ko‘ring!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Menga kasallik yoki alomatlaringizni yozing, men yordam beraman!")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

