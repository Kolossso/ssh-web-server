import os
import paramiko
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message

# Получаем токен из переменной окружения
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не задан в переменных окружения")

# Данные для SSH-подключения
VPS_HOST = "34.88.223.194"
VPS_PORT = 22
VPS_USER = "zokirjonovjavohir61"
PRIVATE_KEY = os.getenv("SSH_PRIVATE_KEY")
START_SCRIPT_PATH = "/home/zokirjonovjavohir61/.steam/steam/steamapps/common/Counter-Strike Global Offensive/game/bin/linuxsteamrt64/start.sh"

# Проверка наличия приватного ключа
if not PRIVATE_KEY:
    raise ValueError("SSH_PRIVATE_KEY не задан в переменных окружения")

# Создаем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🚀 Запустить сервер CS2")]],
    resize_keyboard=True
)

# Асинхронная функция для выполнения SSH-команд
async def run_ssh_command(command: str) -> str:
    try:
        key = paramiko.RSAKey.from_private_key_file("id_rsa")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, pkey=key)

        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        ssh.close()

        return output if output else stderr.read().decode()
    except Exception as e:
        return f"Ошибка SSH: {str(e)}"

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Нажми кнопку для запуска сервера CS2:", reply_markup=keyboard)

# Обработчик кнопки запуска сервера
@dp.message(F.text == "🚀 Запустить сервер CS2")
async def run_server(message: Message):
    await message.answer("Запускаю сервер CS2... 🕹")
    result = await run_ssh_command(f"bash {START_SCRIPT_PATH}")
    await message.answer(f"Результат:\n{result}")

# Функция запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
