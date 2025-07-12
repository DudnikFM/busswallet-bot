import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN переменная окружения не задана")

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("TRC20", callback_data='TRC20'), InlineKeyboardButton("BEP20", callback_data='BEP20')],
        [InlineKeyboardButton("ERC20", callback_data='ERC20'), InlineKeyboardButton("BTC", callback_data='BTC')],
        [InlineKeyboardButton("SOL", callback_data='SOL')],
        [InlineKeyboardButton("❌ Отменить", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите сеть, в которой хотите оплатить:", reply_markup=reply_markup)

# Обработчик кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choice = query.data
    if choice == 'cancel':
        await query.edit_message_text("Обратитесь в техподдержку. К сожалению, не удаётся обнаружить ваш платёж. Напишите, пожалуйста, в Telegram: @secondlang_support")
    else:
        await query.edit_message_text(f"Вы выбрали сеть: {choice}")

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
