
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

TOKEN = "8122510813:AAHOpgwNJqUWUhuo01Wl0FywRS40sBARhR0"
CHAT_ID = "7786764846"
WALLETS = {
    "TRC20": "TQw19dGhSNeryY3eDX3byeD4KsThyNdCLU",
    "BEP20": "0x7a210fc89eccfaed2ea25cc27446e44743533ac2",
    "ERC20": "0x7a210fc89eccfaed2ea25cc27446e44743533ac2",
    "BTC": "1G7pG7WQwTvmmND9RgQFzkEQyuq9WAWeM3",
    "SOL": "3uUsgFUUUJLx5rYJ786rgcBozaxtFLvoSv1a2xvfbKrh"
}

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("TRC20", callback_data='TRC20')],
        [InlineKeyboardButton("BEP20", callback_data='BEP20')],
        [InlineKeyboardButton("ERC20", callback_data='ERC20')],
        [InlineKeyboardButton("BTC", callback_data='BTC')],
        [InlineKeyboardButton("SOL", callback_data='SOL')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите сеть для оплаты:", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    network = query.data
    address = WALLETS[network]
    message = f"💸 <b>Отправьте $35</b> на адрес в сети <b>{network}</b>:

<code>{address}</code>

После отправки нажмите кнопку ниже."
    keyboard = [[InlineKeyboardButton("✅ Я оплатил", callback_data='paid')],
                [InlineKeyboardButton("❌ Отменить", callback_data='cancel')]]
    query.edit_message_text(text=message, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

def paid(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user = query.from_user
    context.bot.send_message(chat_id=CHAT_ID, text=f"💰 <b>Оплата</b> от @{user.username or user.first_name}
Нужно проверить и подтвердить вручную.", parse_mode='HTML')
    query.edit_message_text("Платёж отправлен. Ожидайте подтверждение.")

def cancel(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text("Обратитесь в техподдержку. К сожалению, не удаётся обнаружить ваш платёж. Напишите, пожалуйста, в Telegram: @secondlang_support")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button, pattern='^(TRC20|BEP20|ERC20|BTC|SOL)$'))
    dp.add_handler(CallbackQueryHandler(paid, pattern='^paid$'))
    dp.add_handler(CallbackQueryHandler(cancel, pattern='^cancel$'))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
