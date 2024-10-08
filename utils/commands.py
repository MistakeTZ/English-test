from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from loader import dp, bot
from os import path

from config import get_env
import utils.kb as kb
from support.messages import message, send_message
from states import UserState
from user import *


# Команда старта бота
@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    id = msg.from_user.id
    print(id)
    users[str(id)] = User(id)
    await send_message(msg, "start", kb.buttons("begin"), state, UserState.default)


# Команда меню
@dp.message(Command("words"))
async def command_settings(msg: Message, state: FSMContext) -> None:
    id = msg.from_user.id
    rus, eng = users[str(id)].get_known() 
    await send_message(msg, "your_know_words", None, None, None, rus, eng)

    