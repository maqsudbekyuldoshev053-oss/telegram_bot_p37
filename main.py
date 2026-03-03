import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import settings
from models.categorys import Category


ADMIN_id = settings.ADMIN_ID


dp = Dispatcher()



class Form(StatesGroup):
    add_new_category = State()
    vacancy_title = State()
    vacancy_salary = State()



@dp.message(Command('add_category'))
async def vacancy_handler(message: Message, state: FSMContext):
    await state.set_state(Form.add_new_category)
    await message.answer("Categorya kiriting:")


@dp.message(Form.add_new_category)
async def add_category_handled(message: Message, state: FSMContext):
    new_category_name = (message.text or "").strip()
    if not new_category_name:
        await message.answer("Kategoriya nomi bo'sh bo'lmasligi kerak. Qayta yuboring.")
        return

    existing = Category.filter(name=new_category_name).first()
    if existing:
        await state.clear()
        await message.answer(f"Bu nomdagi kategoriya allaqachon mavjud: {existing.name}")
        return

    Category.create(name=new_category_name)
    await state.clear()
    await message.answer(f"Yangi {new_category_name} nomli categorya database ga qo'shildi.")




@dp.message(Command("add_vacancy"))
async def add_vacancy_handled(message: Message, state: FSMContext):
    categorys = Category.get_all()
    await state.set_state(Form.vacancy_title)

    if not categorys:
        await message.answer("Hozircha kategoriyalar mavjud emas. Avval /add_category orqali qo'shing.")
        return

    ikm = InlineKeyboardBuilder()
    for category in categorys:
        ikm.add(
            InlineKeyboardButton(text=category.name, callback_data=f"category:{category.id}")
        )
    ikm.adjust(1)
    await message.answer('Vacancies', reply_markup=ikm.as_markup(resize_keyboard=True))
    await message.answer("Ish nomini kiriting:")



@dp.message(Form.vacancy_title)
async def vacancy_title_handler(message: Message, state: FSMContext):
    title = (message.text or "").strip()

    await state.update_data(title=title)
    await state.set_state(Form.vacancy_salary)

    await message.answer("Oylikni kiriting (kamida 500000 so'm):")




@dp.message(Form.vacancy_salary)
async def vacancy_salary_handler(message: Message, state: FSMContext):
    try:
        salary = int(message.text.replace(" ", ""))
    except:
        await message.answer("Iltimos faqat raqam kiriting.")
        return

    if salary < 500000:
        await message.answer("Oylik kamida 500 000 so'm bo'lishi kerak.")
        return

    data = await state.get_data()

    title = data.get("title")

    await message.answer(
        f"✅ Vakansiya qo'shildi:\n\n"
        f"Ish nomi: {title}\n"
        f"Oylik: {salary} so'm"
    )
    await state.clear()



@dp.message(CommandStart)
async def start_handler(message: Message):
    await message.reply('Xush kelibsiz')



async def main():
    bot = Bot(settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())










