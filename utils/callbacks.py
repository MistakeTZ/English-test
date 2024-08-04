from aiogram import F
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from loader import dp, bot
import asyncio
from os import path

from config import get_env, get_config

import utils.kb as kb
from user import users
from support.messages import get_text, send_message
from states import UserState


# Начало
@dp.callback_query(F.data == "begin")
async def menu_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    id = clbck.from_user.id
    await send_message(clbck, "word", None, state, UserState.guess, users[str(id)].get_next()[0])


# Начинается с
@dp.callback_query(F.data.startswith("guess_"))
async def city_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    answer = clbck.data[-1] 
    id = clbck.from_user.id
    user = users[str(id)]
    if answer == "y":
        user.guess_word(True)
    elif answer == "n":
        user.guess_word(False)
    else:
        user.change_lang()
        await clbck.message.edit_reply_markup(reply_markup=kb.table(3, 1, "✅", "guess_y", get_text("change_lang") + " ✅", "guess_l", "❌", "guess_n"))
        return
    await send_message(clbck, "word", None, None, None, user.get_next()[0])
    if answer == "y":
        user.save()


