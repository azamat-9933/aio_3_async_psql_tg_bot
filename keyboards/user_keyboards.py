from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def generate_languages_buttons():
    builder = InlineKeyboardBuilder()
    builder.button(text='Русский 🇷🇺', callback_data='ru')
    builder.button(text='English 🇬🇧', callback_data='en')
    builder.adjust(2)
    return builder.as_markup()

async def generate_send_contact_button(language):
    builder = ReplyKeyboardBuilder()
    if language == "ru":
        builder.button(text="Отправить контакт 📲", request_contact=True)
    elif language == "en":
        builder.button(text="Send contact 📲", request_contact=True)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


async def generate_submitting_keyboards(language):
    builder = ReplyKeyboardBuilder()
    if language == "ru":
        builder.button(text="Подтвердить ✅")
        builder.button(text="Отклонить ❌")
    elif language == "en":
        builder.button(text="Confirm ✅")
        builder.button(text="Decline ❌")
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)

async def generate_main_menu_buttons(language):
    builder = ReplyKeyboardBuilder()
    if language == "ru":
        builder.row(KeyboardButton(text="Каталог товаров 📚"))
        builder.row(KeyboardButton(text="Настройки ⚙"))
        builder.row(KeyboardButton(text="Оставить отзыв ✍🏻"))
    elif language == "en":
        builder.row(KeyboardButton(text="Product catalog 📚"))
        builder.row(KeyboardButton(text="Settings ⚙"))
        builder.row(KeyboardButton(text="Leave feedback ✍🏻"))

    return builder.as_markup(resize_keyboard=True)
