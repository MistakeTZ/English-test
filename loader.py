from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from user import load_words
from config import get_env, load_env
from support import messages

# Загрузка сообщений
messages.load_messages()

# Загрузка слов
load_words()

# Загрузка файлов окружения
load_env()


# Создание бота
bot = Bot(get_env("token"), default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
