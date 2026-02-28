import asyncio
import logging
import sys
from datetime import datetime

import csv
import json
from gc import callbacks
from pyexpat.errors import messages

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, InlineKeyboardButton, BotCommand, BotCommandScopeAllPrivateChats, CallbackQuery, \
    InputMediaPhoto, InputMediaVideo, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import engine
from models import District, Region
from sqlalchemy import text


TOKEN = "7874681745:AAFb_km4wx4lHNfD-MAYK9OmabOhLdB0ORs"
redis_url = 'redis://localhost:6379/0'

dp = Dispatcher(storage=RedisStorage.from_url(redis_url))
ADMIN_ID = 7742819222



@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.reply("Xush kelibsiz")


    regions = Region.get_all()
    ikm = InlineKeyboardBuilder()
    for region in regions:
        ikm.add(
            InlineKeyboardButton(text=region.name,
            callback_data=f"region:{region.id}")
            )
    ikm.adjust(1)
    await message.reply("Viloyatni tanlang:", reply_markup=ikm.as_markup())


@dp.callback_query(F.data.startswith("region:"))
async def region_handler(callback: CallbackQuery) -> None:
    region_id = callback.data.removeprefix("region:")

    districts = District.get_all()
    ikm = InlineKeyboardBuilder()

    for district in districts:
        ikm.button(
            text=district.name, callback_data=f"district:{district.id}"
        )
    ikm.adjust(1)
    await callback.message.edit_reply_markup(callback.inline_message_id, reply_markup=ikm.as_markup())

    ikm.button(text="🔙 Back", callback_data='back')
    ikm.adjust(1)
    await callback.message.edit_text("Tumanni tanlang:",reply_markup=ikm.as_markup())


@dp.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery) -> None:

    regions = Region.get_all()
    ikm = InlineKeyboardBuilder()
    for region in regions:
        ikm.add(
            InlineKeyboardButton(text=region.name,
                                 callback_data=f"region:{region.id}")
        )
    ikm.adjust(1)
    await callback.message.edit_text("Viloyatni tanlang:", reply_markup=ikm.as_markup())

    await callback.answer()


@dp.callback_query(F.data.startswith("district:"))
async def district_handler(callback: CallbackQuery) -> None:
    msg = callback.data.removeprefix("district:")
    await callback.answer(msg + " Tanlandi", show_alert=True)



@dp.message(Command("migrate"))
async def migrate(message: Message):

    with open("regions.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Region.create(name=row["name"])

    with open("districts.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            District.create(
                id=int(row["id"]),name=row["name"], region_id=int(row["region_id"]))


    await message.answer("Region va District ma’lumotlari databasega yozildi!✅")



async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    # dp.startup.register(startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

