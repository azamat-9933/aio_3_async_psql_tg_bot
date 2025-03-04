from aiogram import Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import async_sessionmaker

from keyboards.user_keyboards import *
from database.user_queries import *
from database.tables import engine
from messages import messages
from messages import generate_submit_message
from states.feedback_state import FeedbackStatesGroup
from states.main_menu_state import MainMenuStatesGroup
from states.registration_state import RegistrationStatesGroup
from configs import FEEDBACK_CHANNEL

user_router = Router()

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@user_router.message(CommandStart())
async def start(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    async with AsyncSessionLocal() as session:
        # Берем все chat_id пользователей из БД в виде списка
        tg_users_ids = await get_all_users_tg_ids(session)
        if chat_id not in tg_users_ids:
            await create_user_only_language(session,
                                            chat_id=chat_id)
            await message.answer(text=messages["message_1"],
                                 reply_markup=await generate_languages_buttons())
        elif chat_id in tg_users_ids:
            try:
                user_lang = await get_language_of_user(session, chat_id)
                user_status = await get_status_of_user(session, chat_id)

                if user_status is False:
                    await start_registration(message, bot, state)
                elif user_status is True:
                    await main_menu(message, bot, state)

            except:
                await message.answer(text=messages["message_1"],
                                     reply_markup=await generate_languages_buttons())


@user_router.callback_query(lambda call: call.data in ["ru", "en"])
async def update_language(call: CallbackQuery, bot: Bot, state: FSMContext):
    chat_id = call.message.chat.id
    language = call.data
    message_id = call.message.message_id
    await bot.delete_message(chat_id, message_id)
    async with AsyncSessionLocal() as session:
        await user_language_update(session,
                                   language=language,
                                   chat_id=chat_id)
    await bot.send_message(chat_id=chat_id,
                           text=messages["message_2"][language])

    await start_registration(call.message, bot, state)


async def start_registration(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    async with AsyncSessionLocal() as session:
        language = await get_language_of_user(session,
                                              chat_id=chat_id)

    await bot.send_message(chat_id,
                           text=messages["message_7"][language])

    await ask_user_full_name(message, bot, state)


async def ask_user_full_name(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    async with AsyncSessionLocal() as session:
        language = await get_language_of_user(session,
                                              chat_id=chat_id)

    await bot.send_message(chat_id,
                           text=messages["message_3"][language])

    await state.set_state(RegistrationStatesGroup.wait_full_name)


@user_router.message(RegistrationStatesGroup.wait_full_name)
async def ask_user_phone_number(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    full_name = message.text
    await state.update_data(
        {
            str(chat_id): {
                "full_name": full_name
            }
        }
    )
    async with AsyncSessionLocal() as session:
        language = await get_language_of_user(session,
                                              chat_id=chat_id)
    await bot.send_message(chat_id,
                           text=messages["message_4"][language],
                           reply_markup=await generate_send_contact_button(language))

    await state.set_state(RegistrationStatesGroup.wait_phone_number)


@user_router.message(RegistrationStatesGroup.wait_phone_number)
async def ask_for_submit(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    if message.content_type == "contact":
        phone_number = message.contact.phone_number
    elif message.content_type == "text":
        phone_number = message.text

    data = await state.get_data()
    data[str(chat_id)].update({"phone_number": phone_number})
    async with AsyncSessionLocal() as session:
        language = await get_language_of_user(session,
                                              chat_id=chat_id)
    await bot.send_message(chat_id,
                           text=await generate_submit_message(data[str(chat_id)]['full_name'],
                                                              data[str(chat_id)]['phone_number'],
                                                              language),
                           reply_markup=await generate_submitting_keyboards(language))

    await state.set_state(RegistrationStatesGroup.wait_for_submit)


@user_router.message(RegistrationStatesGroup.wait_for_submit)
async def submit_registration(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()

    async with AsyncSessionLocal() as session:
        language = await get_language_of_user(session,
                                              chat_id=chat_id)

    if "✅" in message.text:
        async with AsyncSessionLocal() as session:
            await register_user(session, chat_id,
                                data[str(chat_id)]['full_name'],
                                data[str(chat_id)]['phone_number']
                                )
        await bot.send_message(chat_id=chat_id,
                               text=messages["message_6"][language])
        del data[str(chat_id)]
        await state.clear()  # TODO: TEST
        await main_menu(message, bot)

    elif "❌" in message.text:
        del data[str(chat_id)]

        await bot.send_message(chat_id=chat_id,
                               text=messages["message_5"][language],
                               reply_markup=ReplyKeyboardRemove())
        await start_registration(message, bot, state)


async def main_menu(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id

    async with AsyncSessionLocal() as session:
        language = await get_language_of_user(session,
                                              chat_id=chat_id)

    await bot.send_message(chat_id=chat_id,
                           text=messages["message_8"][language],
                           reply_markup=await generate_main_menu_buttons(language))

    await state.set_state(MainMenuStatesGroup.main_menu)


# ------------------------------------------------------------------------------------------------
@user_router.message(MainMenuStatesGroup.main_menu)
async def choose_option_main_menu(message: Message, bot: Bot, state: FSMContext):
    if "✍🏻" in message.text:
        await ask_for_feedback_from_user(message, bot, state)
    elif "⚙" in message.text:
        pass
    elif "📚" in message.text:
        pass


# -----------------------------------------------------------------------------
# FEEDBACK SECTION
async def ask_for_feedback_from_user(message: Message, bot: Bot, state: FSMContext):
    chat_id = message.chat.id

    async with AsyncSessionLocal() as session:
        language = await get_language_of_user(session,
                                              chat_id=chat_id)

    await bot.send_message(chat_id=chat_id,
                           text=messages["message_9"][language],
                           reply_markup=await generate_back_button(language))

    await state.set_state(FeedbackStatesGroup.ask_feedback)


@user_router.message(FeedbackStatesGroup.ask_feedback)
async def receive_feedback(message: Message, bot: Bot, state: FSMContext):
    if message.text == "Назад ⬅" or message.text == "Back ⬅":
        await main_menu(message, bot, state)
    else:
        chat_id = message.chat.id
        feedback = message.text

        async with AsyncSessionLocal() as session:
            language = await get_language_of_user(session,
                                                  chat_id=chat_id)

            user_data = await get_user_full_name_phone_number(session, chat_id)

        await bot.send_message(FEEDBACK_CHANNEL,
                               text=f"""Отзыв от пользователя 🔔🔔🔔
\nИмя: {user_data[0]}
\nТелефон: {user_data[1]}
\nОтзыв:
{feedback}""")

        await bot.send_message(chat_id=chat_id,
                               text=messages["message_10"][language])

        await main_menu(message, bot, state)

