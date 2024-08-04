from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
from loader import dp, bot
from datetime import datetime

from os import path
import re
from config import get_env
import asyncio

from user import users
import utils.kb as kb
from support.messages import send_message, get_text
from states import UserState


# Установка электронной почты
@dp.message(UserState.guess)
async def email_check(msg: Message, state: FSMContext):
    id = msg.from_user.id
    user = users[str(id)]
    correct_word = user.get_correct()

    for word in msg.text.lower().split(","):
        if word.strip() in correct_word:
            await msg.react([ReactionTypeEmoji(emoji="👍")])
            await send_message(msg, "word", None, None, None, user.get_next()[0])
            user.guess_word(True)
            user.save()
            return
    else:
        await send_message(msg, "correct_is", kb.table(3, 1, "✅", "guess_y", get_text("change_lang"), "guess_l", "❌", "guess_n"), 
                           None, None, ", ".join(correct_word))



# Установка времени
@dp.message(UserState.time)
async def time_check(msg: Message, state: FSMContext):
    try:
        time = datetime.strptime(msg.text, "%H:%M")
    except:
        await send_message(msg, "wrong_time")
        return
