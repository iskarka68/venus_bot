import logging
import random
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

# Подключение к базе данных
conn = sqlite3.connect("venus.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    coins INTEGER DEFAULT 0,
    vcoins INTEGER DEFAULT 0,
    inventory TEXT DEFAULT ''
)''')
conn.commit()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    await message.reply("Добро пожаловать на Венеру! Напиши /profile, чтобы посмотреть свой профиль.")

@dp.message_handler(commands=['profile'])
async def profile(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT coins, vcoins, inventory FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        coins, vcoins, inventory = row
        await message.reply(f"Профиль Венерианца:
Монеты: {coins}
Венериумы: {vcoins}
Инвентарь: {inventory or 'пусто'}")
    else:
        await message.reply("Сначала напиши /start")

@dp.message_handler(commands=['mine'])
async def mine(message: types.Message):
    user_id = message.from_user.id
    amount = random.randint(100, 500)
    cursor.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    await message.reply(f"Ты добыл {amount} монет в шахте.")

@dp.message_handler(commands=['farm'])
async def farm(message: types.Message):
    user_id = message.from_user.id
    amount = random.randint(50, 300)
    cursor.execute("UPDATE users SET coins = coins + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()
    await message.reply(f"Ты вырастил урожай на {amount} монет.")

@dp.message_handler(commands=['exchange'])
async def exchange(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT coins FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row and row[0] >= 1_000_000:
        cursor.execute("UPDATE users SET coins = coins - 1000000, vcoins = vcoins + 1 WHERE user_id = ?", (user_id,))
        conn.commit()
        await message.reply("Ты обменял 1,000,000 монет на 1 венериум.")
    else:
        await message.reply("Недостаточно монет для обмена (нужно 1,000,000).")

@dp.message_handler(commands=['random'])
async def random_number(message: types.Message):
    num = random.randint(1, 100)
    await message.reply(f"Случайное число: {num}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
