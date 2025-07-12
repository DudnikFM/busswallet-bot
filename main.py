import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN переменная окружения не задана")

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("TRC20", callback_data='TRC20'), InlineKeyboardButton("BEP20", callback_data='BEP20')],
        [InlineKeyboardButton("ERC20", callback_data='ERC20'), InlineKeyboardButton("BTC", callback_data='BTC')],
        [InlineKeyboardButton("SOL", callback_data='SOL')],
        [InlineKeyboardButton("❌ Отменить", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите сеть, в которой хотите оплатить:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "cancel":
        query.edit_message_text("Обратитесь в техподдержку. К сожалению, не удаётся обнаружить ваш платёж. Напишите, пожалуйста, в Telegram: @secondlang_support")
    else:
        query.edit_message_text(f"Вы выбрали сеть: {query.data}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
