from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import Router, F
from filters.admin import IsAdmin
from keyboards.reply import admin_menu

router = Router()

@router.message(CommandStart(), IsAdmin())
async def start(message: Message):
    await message.answer("Assalomu alaykum! Admin paneliga xush kelibsiz!", reply_markup=admin_menu)

@router.message(F.text == "Orqaga", IsAdmin())
async def ortga(message: Message):
    await message.answer("Ortga qaytildi!", reply_markup=admin_menu)

@router.message(IsAdmin())
async def admin(message: Message):
    pass
