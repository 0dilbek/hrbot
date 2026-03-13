from aiogram import Router, F
from aiogram.types import Message
from filters.admin import IsAdmin
from utils.excel_report import generate_report
from aiogram.types import BufferedInputFile
from aiogram.fsm.context import FSMContext
from states.admin import GetSertificateFIleState
from keyboards.reply import reports_menu, back_btn
from database.models import TeacherResume, TgUser

router = Router()

@router.message(F.text == "Hisobotlar", IsAdmin())
async def open_report_menu(message: Message):
    await message.answer("Hisobotlar bo'limidasiz", reply_markup=reports_menu)

@router.message(F.text == "Excel hisobot", IsAdmin())
async def send_report(message: Message):
    buffer = await generate_report()
    file = BufferedInputFile(buffer.read(), filename="reports.xlsx")
    await message.answer_document(file, caption="Hisobot")

@router.message(F.text == "Sertifikatni ko‘rish", IsAdmin())
async def show_sertificates(message: Message, state: FSMContext):
    await state.set_state(GetSertificateFIleState.tg_id)
    await message.answer("Sertifikat fayllarini olish uchun arizachining telegram id raqamini yuboring.", reply_markup=back_btn)

@router.message(F.text == "Orqaga", GetSertificateFIleState.tg_id)
async def back(message: Message, state: FSMContext):
    await message.answer("Orqaga qaytdik!!", reply_markup=reports_menu)
    await state.clear()

@router.message(GetSertificateFIleState.tg_id, F.text.isdigit())
async def get_sertificate_file(message: Message, state: FSMContext):
    tg_id = int(message.text)
    user = await TgUser.get_or_none(tg_id=tg_id)
    if not user:
        await message.answer("Bunday foydalanuvchi topilmadi")
        return
    resume = await TeacherResume.filter(user=user).exclude(sertificates=[]).last()
    if not resume:
        await message.answer("Bu foydalanuvchining sertifikatlari topilmadi")
        return
    for sertificate in resume.sertificates:
        if sertificate.get("content_type") == "document":
            await message.answer_document(sertificate.get("file_id"), caption=f"{user.full_name} - {sertificate.get('name')} - {sertificate.get('ball')}")
        else:
            await message.answer_photo(sertificate.get("file_id"), caption=f"{user.full_name} - {sertificate.get('name')} - {sertificate.get('ball')}")
    await state.clear()
    await message.answer("Sertifikat fayllari tugadi", reply_markup=reports_menu)