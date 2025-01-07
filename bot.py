import os
import logging
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Loggingni sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot tokeni va kanal URL'ini o‘zgartiring
TELEGRAM_BOT_TOKEN = "5205989916:AAHqjHNVC2nNjmF0cX9AO7FoZaIVVVYzlDk"  # Tokenni shu yerga yozing
CHANNEL_URL = '@yanvaristik'  # Kanal nomi yoki URL

# Maxsus tokenni bot egasini aniqlash uchun
OWNER_TOKEN = '67695onam'

# Botni boshlash
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Bot ishga tushdi!')

# Kanalga obuna bo‘lmagan foydalanuvchilarni tekshirish
async def check_subscription(update: Update, context: CallbackContext) -> None:
    if update.message:  # Faqat xabar bo'lsa ishlaydi
        user = update.message.from_user
        chat_id = update.message.chat_id
        user_name = user.username if user.username else "N/A"  # Foydalanuvchining username'ini olish

        # Foydalanuvchi kanalga obuna bo‘lganini tekshirish
        try:
            member = await context.bot.get_chat_member(CHANNEL_URL, user.id)
            if member.status == 'left':  # Agar foydalanuvchi obuna bo‘lmagan bo‘lsa
                await update.message.delete()  # Foydalanuvchining xabarini o‘chirish
                warning_message = await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"Siz {CHANNEL_URL} kanaliga obuna bo'lmagansiz, shuning uchun xabaringiz o'chirildi. "
                         "Guruhga faqat kanalga obuna bo'lsangizgina yozishingiz mumkin.\n"
                         f"Ogohlantirish foydalanuvchi: {user_name} (@{user_name} yoki ID: {user.id})"
                )
                
                # 20 soniyadan keyin ogohlantirish xabarini o‘chirish
                time.sleep(20)
                await context.bot.delete_message(chat_id=chat_id, message_id=warning_message.message_id)
        except Exception as e:
            logger.error(f"Xatolik: {e}")

# Bot egasiga boshqaruv ruxsatini berish
async def grant_admin(update: Update, context: CallbackContext) -> None:
    if update.message.text.split()[1] == OWNER_TOKEN:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Sizga botni boshqarish huquqi berildi!"
        )

# Xabarlar uchun filterning ishlashi
async def handle_messages(update: Update, context: CallbackContext) -> None:
    await check_subscription(update, context)

# Asosiy funksiyalarni boshlash
def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    # Botni ishga tushurish
    application.run_polling()

if __name__ == '__main__':
    main()
