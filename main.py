import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройки логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
TEST_FORM_URL = os.getenv("TEST_FORM_URL")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Подтвердить оплату", callback_data='confirm')],
        [InlineKeyboardButton("❌ Отменить", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("После отправки оплаты нажмите кнопку ниже.", reply_markup=reply_markup)

# Обработка кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'confirm':
        await context.bot.send_message(chat_id=query.from_user.id, text="✅ Платёж подтверждён. Переходите по ссылке: " + TEST_FORM_URL)
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"💸 Оплата подтверждена от @{query.from_user.username or 'пользователя без username'}")
    elif query.data == 'cancel':
        await context.bot.send_message(chat_id=query.from_user.id, text="Обратитесь в техподдержку. К сожалению, не удаётся обнаружить ваш платёж. Напишите, пожалуйста, в Telegram: @secondlang_support")
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"🚫 Оплата отменена пользователем @{query.from_user.username or 'без username'}")

# Запуск бота
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
