import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

TOKEN = "8122510813:AAHOpgwNJqUWUhuo01Wl0FywRS40sBARhR0"
ADMIN_CHAT_ID = "7786764846"

WALLETS = {
    "TRC20": "TQw19dGhSNeryY3eDX3byeD4KsThyNdCLU",
    "BEP20": "0x7a210fc89eccfaed2ea25cc27446e44743533ac2",
    "ERC20": "0x7a210fc89eccfaed2ea25cc27446e44743533ac2",
    "BTC": "1G7pG7WQwTvmmND9RgQFzkEQyuq9WAWeM3",
    "SOL": "3uUsgFUUUJLx5rYJ786rgcBozaxtFLvoSv1a2xvfbKrh"
}

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("TRC20", callback_data='TRC20')],
        [InlineKeyboardButton("BEP20", callback_data='BEP20')],
        [InlineKeyboardButton("ERC20", callback_data='ERC20')],
        [InlineKeyboardButton("BTC", callback_data='BTC')],
        [InlineKeyboardButton("SOL", callback_data='SOL')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Выберите сеть для оплаты:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    network = query.data
    wallet = WALLETS.get(network)
    message = f"💳 <b>Отправьте $35</b> на адрес в сети <b>{network}</b>: 
<code>{wallet}</code>"
    keyboard = [
        [InlineKeyboardButton("✅ Я оплатил", callback_data=f"confirm_{network}")],
        [InlineKeyboardButton("❌ Отменить", callback_data="cancel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=message, parse_mode='HTML', reply_markup=reply_markup)

def confirm(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user
    network = query.data.split("_")[1]
    wallet = WALLETS.get(network)
    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"🧾 Новый запрос на открытие счёта
"
            f"Имя: {user.full_name}
"
            f"Юзер: @{user.username}
"
            f"Сеть: {network}
"
            f"Кошелёк: {wallet}

"
            f"Подтвердите оплату и отправьте пользователю номер счёта вручную."
        )
    )
    query.edit_message_text("Спасибо! Ваша заявка на открытие счёта отправлена. Ожидайте подтверждения.")

def cancel(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.edit_message_text("Обратитесь в техподдержку. К сожалению, не удаётся обнаружить ваш платёж. Напишите, пожалуйста, в Telegram: @secondlang_support")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(confirm, pattern='^confirm_'))
    dispatcher.add_handler(CallbackQueryHandler(cancel, pattern='^cancel$'))
    dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
