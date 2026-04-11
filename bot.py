from config import (
    BOT_TOKEN,
    REDIS_HOST,
    REDIS_PORT,
    BOT_API_SERVER,
    BOT_PROXY_URL,
    WEBHOOK_BASE_URL,
    WEBHOOK_PATH,
    WEBHOOK_LISTEN_HOST,
    WEBHOOK_LISTEN_PORT,
)
import asyncio
from aiogram import Bot, Dispatcher, Router, BaseMiddleware
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from handlers import router as main_router
from logging import basicConfig, INFO, getLogger
from database import init_db, close_db
from miidlewares.base import LongMessageMiddleware

logger = getLogger(__name__)

storage = RedisStorage.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")

dp = Dispatcher(storage=storage)
debug_router = Router()


class UpdateDebugMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        message = getattr(event, "message", None)
        if message and message.from_user:
            logger.info(
                "Incoming message user_id=%s chat_id=%s text=%r",
                message.from_user.id,
                message.chat.id,
                message.text,
            )
        return await handler(event, data)


async def set_webhook_with_retry(bot: Bot):
    webhook_url = f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}"
    await asyncio.sleep(2)

    for attempt in range(1, 11):
        try:
            await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
            logger.info("Webhook set: %s", webhook_url)
            return
        except TelegramNetworkError as e:
            logger.warning("Webhook set attempt %s failed: %s", attempt, e)
            await asyncio.sleep(2)

    raise RuntimeError("Failed to set webhook after retries")


async def on_startup(bot: Bot):
    await init_db()
    asyncio.create_task(set_webhook_with_retry(bot))


async def on_shutdown(bot: Bot):
    try:
        await bot.delete_webhook()
    except TelegramNetworkError as e:
        logger.warning("Webhook delete failed: %s", e)
    await close_db()
    await bot.session.close()


@debug_router.message()
async def unhandled_message(message: Message):
    logger.info("Unhandled message user_id=%s text=%r", message.from_user.id, message.text)
    await message.answer("Xabar qabul qilindi, lekin mos handler topilmadi. /start yuboring.")


def main():
    bot_api_server = TelegramAPIServer.from_base(BOT_API_SERVER, is_local=True)
    bot_session = AiohttpSession(proxy=BOT_PROXY_URL) if BOT_PROXY_URL else AiohttpSession()
    if BOT_PROXY_URL:
        logger.info("Proxy enabled for Telegram API requests")
    bot = Bot(token=BOT_TOKEN, server=bot_api_server, session=bot_session)

    dp.include_router(main_router)
    dp.include_router(debug_router)
    dp.update.middleware(UpdateDebugMiddleware())
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
