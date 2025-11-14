import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from handlers.user import user_router
from keyboards.menu_commands import set_main_menu
from services.file_handling import prepare_docs

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Задаём базовую конфигурацию логирования
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
    )
    # Выводим в консоль информацию о начале запуска бота
    logger.info("Starting bot")

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Загружаем документы
    logger.info("Preparing docs")
    docs, embeddings = prepare_docs("data")
    logger.info("The docs is uploaded. Total docs: %d", len(docs))

    # Инициализируем "базу данных"
    db: dict = {}

    # Сохраняем документы и "базу данных" в `workflow_data`
    dp.workflow_data.update(docs=docs, embeddings=embeddings, db=db)

    # Настраиваем главное меню команд бота
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())