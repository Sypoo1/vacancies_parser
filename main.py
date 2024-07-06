import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from dotenv import load_dotenv
from handlers.handlers import router
from aiogram.utils.chat_action import ChatActionMiddleware


load_dotenv()
host: str = getenv("host")
Bot_Token: str = getenv("Bot_Token")
bot: Bot = Bot(token=Bot_Token)



async def main() -> None:
    try:
        logging.info("вызвана функция main")

        redis: Redis = Redis(host=host, port=6379, )
        await redis.flushdb()
        storage: RedisStorage = RedisStorage(redis=redis)

        dp: Dispatcher = Dispatcher(storage=storage)
        dp.include_router(router)
        dp.message.middleware(ChatActionMiddleware())

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


    except Exception as error:
        logging.error(f" user_id = 666 ;;; ошибка: {error}", exc_info=True)  # user_id = 666 означает ошибку



if __name__ == "__main__":
    try:
        logging.basicConfig(
            level=logging.INFO,
            filename="logs/main.log",
            filemode="a",
            format="%(asctime)s ;;; %(levelname)s ;;; %(message)s",
            encoding="utf-8",
        )

        logging.info("запуск бота")  

        asyncio.run(main())

    except (KeyboardInterrupt, SystemExit):
        logging.info("выключение бота через терминал")
        print("Bot stopped")
    except Exception as error:
        print("Bot stopped")
        logging.error(f"ошибка: {error}", exc_info=True)
