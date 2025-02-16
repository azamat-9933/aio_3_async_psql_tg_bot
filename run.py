import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.user_handlers import user_router
from configs import TOKEN

dp = Dispatcher()

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp.include_routers(user_router)





async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())