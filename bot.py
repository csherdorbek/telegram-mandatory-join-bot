import logging
import time
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Maxfiy ma'lumotlar
BOT_TOKEN = "5205989916:AAHqjHNVC2nNjmF0cX9AO7FoZaIVVVYzlDk"
ADMIN_TOKEN = "67695onam"
CHANNEL_USERNAME = "@yanvaristik"

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Foydalanuvchini kanalga a'zo ekanligini tekshirish funksiyasi
def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Xato: {e}")
        return False

# Guruhdagi xabarlarni filtr qilish
def filter_messages(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username
    message = update.message

    # Foydalanuvchini kanalga a'zo ekanligini tekshirish
    if not check_subscription(context.bot, user_id):
        # Foydalanuvchi xabarini o'chirish
        message.delete()

        # Ogohlantirish xabarini yuborish
        warning_msg = (
            f"@{username}, siz {CHANNEL_USERNAME} kanaliga obuna bo‘lmagansiz.\n"
            "Shuning uchun xabaringiz o‘chirildi. Guruhda yozish uchun kanalga obuna bo‘ling."
        )
        sent_message = message.reply_text(warning_msg)

        # 15 soniyadan keyin ogohlantirish xabarini o'chirish
        time.sleep(15)
        sent_message.delete()

# Admin boshqaruvi
def admin_control(update: Update, context: CallbackContext):
    if update.message.text == ADMIN_TOKEN:
        update.message.reply_text("Botning qo'lda boshqaruvi faollashtirildi.")
    else:
        update.message.reply_text("Noto'g'ri token kiritildi.")

# /start komandasi
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Assalomu alaykum! Ushbu bot guruh uchun majburiy aʼzo funksiyasini ta'minlaydi.\n"
        f"Guruhda yozish uchun {CHANNEL_USERNAME} kanaliga obuna bo‘ling."
    )

# Asosiy funksiya
def main():
    # Updater va Dispatcher yaratish
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    # Komanda uchun handler
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.private, admin_control))

    # Guruh xabarlarini filtrlash uchun handler
    dispatcher.add_handler(MessageHandler(Filters.group, filter_messages))

    # Botni ishga tushirish
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()