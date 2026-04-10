from config import (
    BOT_TOKEN,
    REDIS_HOST,
    REDIS_PORT,
    BOT_API_SERVER,
    WEBHOOK_BASE_URL,
    WEBHOOK_PATH,
    WEBHOOK_LISTEN_HOST,
    WEBHOOK_LISTEN_PORT,
)
from aiogram import Bot, Dispatcher
from aiogram.client.telegram import TelegramAPIServer
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from handlers import router as main_router
from logging import basicConfig, INFO
from database import init_db, close_db
from miidlewares.base import LongMessageMiddleware

storage = RedisStorage.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")

dp = Dispatcher(storage=storage)

async def on_startup(bot: Bot):
    await init_db()
    await bot.set_webhook(url=f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}", drop_pending_updates=True)


async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    await close_db()


def main():
    bot_api_server = TelegramAPIServer.from_base(BOT_API_SERVER)
    bot = Bot(token=BOT_TOKEN, server=bot_api_server)

    dp.include_router(main_router)
    dp.update.middleware(LongMessageMiddleware())
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEBHOOK_LISTEN_HOST, port=WEBHOOK_LISTEN_PORT)

if __name__ == "__main__":
    basicConfig(level=INFO)
    main()
