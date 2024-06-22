from aiogram.enums import ParseMode
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from telegram.ext import CommandHandler

from config import TOKEN
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
import asyncio

from db.engine import sessionmaker, create_db
from db.orm_query import create_question, create_answer
from middlewares.db import DBMiddleware


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(mess: types.Message):
    await mess.answer(text='Добро пожаловать в техподдержку, какой у Вас вопрос?')

@dp.message((F.text) & (F.chat.id != 5097236355))
async def question(mess: types.Message, session: AsyncSession):
    await create_question(mess.chat.id, mess.text, session)
    await bot.send_message(chat_id=5097236355, text=mess.text)

    await mess.answer(text='<i>Ваш вопрос отправлен, ожидайте ответ от специалиста.</i>', parse_mode=ParseMode.HTML)

@dp.message((F.reply_to_message) & (F.chat.id != 5097236355))
async def answer(mess: types.Message, session):
    chat_id = await create_answer(mess.reply_to_message.text, session)
    await bot.send_message(chat_id=chat_id, text=f'\
<b>Ответ от техподдержки:</b>\n\
{mess.text}\
', parse_mode=ParseMode.HTML)

    await mess.answer(text='<i>Ответ отправлен.</i>', parse_mode=ParseMode.HTML)

async def starup():
    await create_db()
async def main():
    dp.startup.register(starup)
    dp.update.middleware(DBMiddleware(sessionmaker=sessionmaker))

    await dp.start_polling(bot)

asyncio.run(main())
