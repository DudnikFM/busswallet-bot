from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import logging
import os

TOKEN = os.getenv("BOT_TOKEN")  # токен должен быть задан в Railway как переменная окружения
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
        [
            InlineKeyboardButton("TRC20", callback_data='TRC20'),
            InlineKeyboardButton("BEP20", callback_data='BEP20')
        ],
        [
            InlineKeyboardButton("ERC20", callback_data='ERC20'),
            InlineKeyboardButton("BTC", callback_data='BTC')
        ],
        [
            InlineKeyboardButton("SOL", callback_data='SOL')
        ],
        [
            InlineKeyboardButton("❌ Отменить", callback_data='cancel')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Выберите сеть, в которой хотите оплатить:",
        reply_markup=reply_markup
    )


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user = query.from_user
    query.answer()

    network = query.data
    if network == "cancel":
        query.edit_message_text(
            "Обратитесь в техподдержку. К сожалению, не удаётся обнаружить ваш платёж. Напишите, пожалуйста, в Telegram: @secondlang_support"
        )
        return

    wallet = WALLETS.get(network)

    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            "📥 Новый запрос на открытие счёта\n\n"
            f"👤Имя: {user.full_name}\n"
            f"🆔Юзер: @{user.username}\n"
            f"🌐Сеть: {network}\n"
            f"💳Кошелёк: {wallet}\n\n"
            "✅Подтвердите оплату и отправьте пользователю номер счёта вручную."
        )
    )

    query.edit_message_text("Спасибо! Ваша заявка на открытие счёта отправлена. Ожидайте подтверждения.")


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
