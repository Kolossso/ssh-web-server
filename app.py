import os
import paramiko
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Твой API-токен (НЕ публикуй его публично!)
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Данные для SSH-подключения
VPS_HOST = "34.88.223.194"
VPS_PORT = 22
VPS_USER = "zokirjonovjavohir61"
PRIVATE_KEY = os.getenv("SSH_PRIVATE_KEY")  # Храним ключ в переменной окружения
START_SCRIPT_PATH = "/home/zokirjonovjavohir61/.steam/steam/steamapps/common/Counter-Strike Global Offensive/game/bin/linuxsteamrt64/start.sh"

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("🚀 Запустить сервер CS2"))

# Функция для выполнения SSH-команд
def run_ssh_command(command):
    try:
        key = paramiko.RSAKey.from_private_key_file("id_rsa")  # Убедись, что ключ сохранен правильно
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, pkey=key)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        ssh.close()
        return output
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет! Этот бот может запускать сервер CS2.\nНажми кнопку ниже:", reply_markup=keyboard)

# Обработчик кнопки запуска сервера
@dp.message_handler(lambda message: message.text == "🚀 Запустить сервер CS2")
async def run_server(message: types.Message):
    await message.answer("Запускаю сервер CS2... 🕹")
    result = run_ssh_command(f"bash {START_SCRIPT_PATH}")
    await message.answer(f"Результат выполнения:\n{result}")

# Запуск бота
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
