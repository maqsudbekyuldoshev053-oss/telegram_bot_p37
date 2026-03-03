import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import settings

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, FSInputFile
import tempfile, os, aiohttp


redis_url = 'redis://localhost:6379/0'

dp = Dispatcher(storage=RedisStorage.from_url(redis_url))

ADMIN_ID =  7742819222

class HelpState(StatesGroup):
    waiting_for_message = State()

MODULES = {
    "1-module": {
        "1-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_1.py",
        "2-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_2.py",
        "3-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_3.py",
        "4-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_4.py",
        "5-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_5.py",
        "6-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_6.py",
        "7-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_7.py",
        "8-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_8.py",
        "9-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_9.py",
        "10-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_10.py",
        "11-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/lesson_11.py",
        "project": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_1/master/project.py",
    },

    "2-module": {
        "1-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_1.py",
        "2-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_2.py",
        "3-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_3.py",
        "4-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_4.py",
        "5-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_5.py",
        "6-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_6.py",
        "7-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_7.py",
        "8-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_8.py",
        "9-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_9.py",
        "10-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_10.py",
        "11-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/lesson_11.py",
        "amaliy_loyiha_kutubxona2": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/amaliy_loyiha_kutubxona2.py",
        "amaliy_loyiha_kutubxona": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/amaliy_loyiha_kutubxona.py",
        "amaliy_loyiha_market2_filebilan": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/amaliy_loyiha_market2_filebilan.py",
        "amaliy_loyiha_online_market": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_2/master/amaliy_loyiha_online_market.py"
    },

    "3-module": {
        "1-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_1.py",
        "2-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_2.py",
        "3-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_3.py",
        "4-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_4.py",
        "5-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_5.py",
        "6-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_6.py",
        "7-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_7.py",
        "8-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_8.py",
        "9-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_9.py",
        "10-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_10.py",
        "11-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_3/master/lesson_11.py"
    },

    "4-module": {
        "Eslatma uchun": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/TODO",
        "1-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_1.sql",
        "2-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_2.sql",
        "3-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_3.sql",
        "4-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_4.sql",
        "5-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_5.sql",
        "6-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_6.sql",
        "7-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_7.sql",
        "8-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_8.sql",
        "9-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_9.sql",
        "10-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_10.sql",
        "11-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_4/master/lesson_11.sql",

    },
    "5-module":{
        "1-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_5/master/lesson_1.py",
        "2-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_5/master/lesson_2.py",
        "3-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_5/master/lesson_3.py",
        "4-dars": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/module_5/master/lesson_4.py",
        "1-dars_bot": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/telegram_bot_p37/master/bot_project/lesson_1",
        "2-dars_bot": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/telegram_bot_p37/master/bot_project/lesson_2",
        "3-dars_bot": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/telegram_bot_p37/master/bot_project/lesson_3",
        "4-dars_bot": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/telegram_bot_p37/master/bot_project/lesson_4",
        "5-dars_bot": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/telegram_bot_p37/master/bot_project/lesson_5",
        "6-dars_bot": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/telegram_bot_p37/master/bot_project/lesson_6",
        "7-dars_bot": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/telegram_bot_p37/master/bot_project/lesson_7",
        "8-dars_bot": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/telegram_bot_p37/master/bot_project/lesson_8",
        "9-dars_bot": "https://raw.githubusercontent.com/maqsudbekyuldoshev053-oss/telegram_bot_p37/master/bot_project/lesson_9"
    },
}



@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer('Xush kelibsiz')


    await dp.storage.redis.sadd("users", message.from_user.id)

    kb_buttons = [[KeyboardButton(text=module)] for module in MODULES.keys()]
    kb = ReplyKeyboardMarkup(keyboard=kb_buttons, resize_keyboard=True)
    await message.answer("Modullardan birini tanlang:", reply_markup=kb)


@dp.message(Command("help"))
async def help_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(HelpState.waiting_for_message)
    await message.answer("Sizga qanday yordam bera olamiz?\n"
                         "Agar xohlamasangiz, /cancel deb bekor qilishingiz mumkin.")

@dp.message(HelpState.waiting_for_message)
async def helps_handler(message: Message, state: FSMContext):
    user_text = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    await message.bot.send_message(
        ADMIN_ID,
        f"📩 Yangi yordam so'rovchi!\n\n"
        f"👤User: @{username}\n\n"
        f"🆔 ID: <code>{user_id}</code>\n\n"
        f"✉️ Xabar:\n{user_text}"
    )

    await message.answer(
        "✅ Surovingiz qabul qilindi.\n"
        "Tez orada ko‘rib chiqiladi."
    )

    await state.clear()

@dp.message(Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Hech qanday jarayon yo'q")
        return
    await state.clear()
    await message.answer("Jarayon bekor qilindi")


@dp.message(Command('admin'))
async def admin_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer(
        "📊 Admin panel:\n"
        "- /done user_id — so‘rovni hal qilindi deb belgilash"
    )


@dp.message(Command('done'))
async def done_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()
    if len(args) != 2:
        await message.answer("Format: /done user_id")
        return

    try:
        user_id = int(args[1])

        await message.bot.send_message(
            chat_id=user_id,
            text="✅ Sizning so'rovingiz admin tomonidan hal qilindi!"
        )

        await message.answer(f"✅ User {user_id} ga xabar muvaffaqiyatli yuborildi.")

    except ValueError:
        await message.answer("❌ Xato: ID faqat raqamlardan iborat bo'lishi kerak.")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")


@dp.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/broadcast ", "")
    users = await dp.storage.redis.smembers("users")

    for user in users:
        try:
            await message.bot.send_message(int(user), text)
        except:
            pass

    await message.answer("✅ Xabar yuborildi.")


@dp.message(Command("stats"))
async def stats_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    users_count = await dp.storage.redis.scard("users")
    await message.answer(f"👥 Foydalanuvchilar soni: {users_count}")



@dp.message()
async def handle_message(message: Message):
    text = message.text

    if text in MODULES:
        await dp.storage.redis.set(f"user_module:{message.from_user.id}", text)

        buttons = [[KeyboardButton(text=dars)] for dars in MODULES[text].keys()]
        buttons.append([KeyboardButton(text="⬅️ Orqaga")])

        kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
        await message.answer(f"{text} darslari:", reply_markup=kb)
        return

    user_module = await dp.storage.redis.get(f"user_module:{message.from_user.id}")

    if user_module:
        user_module = user_module.decode()
        darslar = MODULES.get(user_module, {})

        if text in darslar:

            await dp.storage.redis.incr(f"lesson:{user_module}:{text}")

            url = darslar[text]

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        await message.answer("Faylni yuklab bo'lmadi")
                        return
                    file_data = await resp.read()
                    file_name = url.split("/")[-1]

            with tempfile.NamedTemporaryFile(delete=False, suffix=file_name) as tmp_file:
                tmp_file.write(file_data)
                tmp_path = tmp_file.name

            await message.answer_document(
                document=FSInputFile(tmp_path, filename=file_name)
            )

            os.remove(tmp_path)
            return


    if text == "⬅️ Orqaga":
        await dp.storage.redis.delete(f"user_module:{message.from_user.id}")

        buttons = [[KeyboardButton(text=module)] for module in MODULES.keys()]
        kb = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

        await message.answer("Modullardan birini tanlang:", reply_markup=kb)
        return

@dp.message(Command("lessons_count"))
async def lessons_count_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda bu komandani ishlatish huquqi yo'q.")
        return

    text_lines = []
    total_downloads = 0

    for module_name, darslar in MODULES.items():
        for dars_name in darslar.keys():
            count = await dp.storage.redis.get(f"lesson:{module_name}:{dars_name}")
            if count is None:
                count = "hali hech kim yuklamadi!"
            else:
                count = int(count)
                total_downloads += count
                text_lines.append(f"• {module_name} - {dars_name}: {count} yuklash")

        text = f"📊 Umumiy yuklangan darslar soni: {total_downloads}\n\n" + "\n".join(text_lines)
        await message.answer(text)



async def main():
    bot = Bot(
        settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())