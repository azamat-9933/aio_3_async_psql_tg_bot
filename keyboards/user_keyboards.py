from aiogram.utils.keyboard import InlineKeyboardBuilder


async def generate_languages_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(text='Русский 🇷🇺', callback_data='ru')
    builder.button(text='English 🇬🇧', callback_data='en')
    builder.adjust(2)
    return builder.as_markup()

