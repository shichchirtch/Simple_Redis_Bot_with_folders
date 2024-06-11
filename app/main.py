import asyncio
from aiogram import Bot, Dispatcher
from handlers.game_handlers import game_router
from handlers.command_handlers import command_router
from bot_base import init_models
from aiogram.enums import ParseMode
from bot_states import redis_storage
from config import settings
from aiogram.client.default import DefaultBotProperties

# Функция конфигурирования и запуска бота
async def main():
    await init_models()
    # Инициализируем бот и диспетчер
    bot = Bot(token=settings.BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=redis_storage)
    # Регистрируем роутеры в диспетчере
    dp.include_router(command_router)
    dp.include_router(game_router)
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())