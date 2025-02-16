from aiogram import F
from aiogram import Bot
from aiogram import Router
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import async_sessionmaker

from keyboards.user_keyboards import *
from database.user_queries import *
from database.tables import engine
from messages import messages

user_router = Router()

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@user_router.message(CommandStart())
async def start(message: Message, bot: Bot):
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
                    # TODO: registration
                    pass
                else:
                    # TODO: main menu
                    pass
            except:
                await message.answer(text=messages["message_1"],
                                     reply_markup=await generate_languages_buttons())



@user_router.callback_query(lambda call: call.data in ["ru", "en"])
async def update_language(call: CallbackQuery, bot: Bot):
    chat_id = call.message.chat.id
    language = call.data
    async with AsyncSessionLocal() as session:
        await user_language_update(session,
                                   language=language,
                                   chat_id=chat_id)
    await bot.send_message(chat_id=chat_id,
                           text=messages["message_2"][language])

