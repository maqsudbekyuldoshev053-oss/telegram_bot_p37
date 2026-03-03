import os
import tempfile

import aiohttp
from aiogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup, FSInputFile

from main import dp


@dp.callback_query(lambda c: c.data.startswith("module:"))
async def module_handler(callback: CallbackQuery):
    module_name = callback.data.split(":")[1]

    dars_buttons = []
    for dars in MODULES[module_name].keys():
        dars_buttons.append([InlineKeyboardButton(text=dars, callback_data=f"dars:{module_name}:{dars}")])

    async with aiohttp.ClientSession() as session:
        async with session.get(dars) as resp:
            if resp.status != 200:
                await callback.message.answer("Faylni yuklab bo'lmadi")
                return

            file_data = await resp.read()
            file_name = dars.split("/")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_name) as tmp_file:
        tmp_file.write(file_data)
        tmp_path = tmp_file.name


    dars_buttons.append(
        [InlineKeyboardButton(text="⬅️ Orqaga",callback_data="back_to_modules")])
    ikm = InlineKeyboardMarkup(inline_keyboard=dars_buttons)

    await callback.message.answer_document(
        document=FSInputFile(tmp_path, filename=file_name),
        reply_markup=dars
    )
    await callback.message.edit_text(
        f"{module_name} darslari:",
        reply_markup=ikm
    )
    os.remove(tmp_path)
