from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from database.tables import TgBotUser
from sqlalchemy.future import select


async def create_user_only_language(session: AsyncSession,
                                    chat_id: int) -> None:
    user = TgBotUser(telegram_id=chat_id)
    session.add(user)
    await session.commit()


async def user_language_update(session: AsyncSession,
                               language: str,
                               chat_id: int) -> None:
    stmt = (
        update(TgBotUser)
        .where(TgBotUser.telegram_id == chat_id)  # Условие: находим пользователя по chat_id
        .values(language=language)  # Обновляем столбец language
    )

    # Выполняем запрос
    await session.execute(stmt)

    # Фиксируем изменения
    await session.commit()


async def get_all_users_tg_ids(session: AsyncSession,):
    # Создаем запрос на получение всех chat_id
    stmt = select(TgBotUser.telegram_id)

    # Выполняем запрос
    result = await session.execute(stmt)
    # Получаем результаты
    tg_ids = [row.telegram_id for row in result]

    return tg_ids

async def get_status_of_user(session: AsyncSession,
                             chat_id: int):
    # Создаем запрос на получение статуса пользователя по chat_id
    stmt = select(TgBotUser.status).where(TgBotUser.telegram_id == chat_id)

    # Выполняем запрос
    result = await session.execute(stmt)
    # Получаем результаты
    status = result.scalar()
    return status


async def get_language_of_user(session: AsyncSession,
                              chat_id: int):
    # Создаем запрос на получение языка пользователя по chat_id
    stmt = select(TgBotUser.language).where(TgBotUser.telegram_id == chat_id)

    # Выполняем запрос
    result = await session.execute(stmt)
    # Получаем результаты
    language = result.scalar()
    return language


async def register_user(session: AsyncSession,
                        chat_id: int,
                        full_name: str,
                        phone_number: str):
    stmt = (
        update(TgBotUser)
        .where(TgBotUser.telegram_id == chat_id)  # Условие: находим пользователя по chat_id
        .values(full_name=full_name,
                phone=phone_number,
                status=True) # Обновляем столбец language
    )

    # Выполняем запрос
    await session.execute(stmt)

    # Фиксируем изменения
    await session.commit()

async def get_user_full_name_phone_number(session, chat_id):
    # Создаем запрос на получение full_name и phone_number пользователя по chat_id
    stmt = select(TgBotUser.full_name, TgBotUser.phone).where(TgBotUser.telegram_id == chat_id)

    # Выполняем запрос
    result = await session.execute(stmt)
    # Получаем результаты
    full_name, phone = result.first()  # ('Azamat', '+998901139933)
    return full_name, phone
