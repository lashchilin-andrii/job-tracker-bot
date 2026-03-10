import asyncio

from aiogram import Bot, Dispatcher

from src.logging import LoggingMiddleware
from src.config import BotConfig
from src.job.handler import router as job_router
from src.user.handler import router as user_router
from src.user_job.handler import router as user_job_router
from src.base.handler import router as base_router

dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(job_router)
dp.include_router(user_job_router)
dp.include_router(base_router)  # Must be last cuz contains fallback handler


dp.message.middleware(LoggingMiddleware())
dp.callback_query.middleware(LoggingMiddleware())


async def main() -> None:
    bot = Bot(token=BotConfig().BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
