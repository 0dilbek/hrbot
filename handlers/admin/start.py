import asyncio
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.exceptions import TelegramNetworkError
from filters.admin import IsAdmin
from keyboards.reply import admin_menu
from logging import getLogger

router = Router()
logger = getLogger(__name__)


async def send_with_retry(message: Message, text: str, reply_markup=None):
    last_error = None
    for attempt in range(1, 4):
        try:
            await message.answer(text, reply_markup=reply_markup, request_timeout=90)
            return
        except TelegramNetworkError as e:
            last_error = e
            logger.warning("Admin reply attempt %s failed: %s", attempt, e)
            await asyncio.sleep(1)
    logger.error("Admin reply failed after retries: %s", last_error)

@router.message(CommandStart(), IsAdmin())
async def start(message: Message):
    await send_with_retry(message, "Assalomu alaykum! Admin paneliga xush kelibsiz!", reply_markup=admin_menu)

@router.message(F.text == "Orqaga", IsAdmin())
async def ortga(message: Message):
    await send_with_retry(message, "Ortga qaytildi!", reply_markup=admin_menu)

@router.message(IsAdmin())
async def admin(message: Message):
    pass
