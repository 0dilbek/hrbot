from database.models import TgUser
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from filters.user import IsRegisteredUser
from aiogram.filters import CommandStart
from keyboards.reply import main_menu_users_btn, vacancies_btn
from keyboards.inline import branches_btn
from aiogram.fsm.context import FSMContext

router = Router()

branches_text = {
    "algoritm": """
<b>Algoritm filiali</b>

Telegram kanalimiz: https://t.me/fitrat_study

Instagram kanalimiz: instagram.com/fitrat_study

Youtube kanalimiz: youtube.com/@fitrat_study

Saytimiz: www.fitrat-study.uz

☎️ +998901149000

Manzil: Toshkent shahar, Uchtepa tumani, Diyorobod MFY 31-mavze.
Mo'ljal: "Korzinka" supermarketining 2-qavati.

🗺 Geolokatsiya: 
https://www.google.com/maps/place/41%C2%B015'50.0%22N+69%C2%B009'13.5%22E/@41.2637685,69.1533616,19.83z/data=!4m4!3m3!8m2!3d41.263876!4d69.1537508?entry=ttu
    """,
    "yangihayot": """
<b>Yangihayot filiali</b>

<b>Telegram kanalimiz:</b> https://t.me/fitrat_yangihayot

<b>Instagram kanalimiz:</b> instagram.com/fitrat_study

<b>Youtube kanalimiz:</b> youtube.com/@fitrat_study

<b>Saytimiz:</b> fitrat-study.uz

<b>📞 +998910899000</b>

<b>Manzil:</b> Toshkent shahar, Yangihayot tumani, Tursunzoda ko‘chasi, 48-uy.
<b>Mo‘ljal:</b> Sergeli 3-metro bekatidan Yangihayot tumani tarafga 450 metr.

<b>🗺 Geolokatsiya:</b> https://maps.app.goo.gl/DYrv3LFLSvDbCL1n6?g_st=com.google.maps.preview.copy
""",
"kesh": """
<b>Kesh filiali</b>

<b>Telegram kanalimiz:</b> https://t.me/Fitrat_study_kesh01

<b>Instagram kanalimiz:</b> https://www.instagram.com/fitrat_study_kesh

<b>Youtube kanalimiz:</b> youtube.com/@fitrat_study

<b>Saytimiz:</b> fitrat-study.uz

<b>📞 +998881679000</b>

<b>Manzil:</b> Shahrisabz shahar, Tutzor MFY, Ipak yo‘li ko‘chasi, 4-uy.
<b>Mo‘ljal:</b> Shahrisabz shahar, "MAKRO" supermarket roʻparasi, "7×7 milliy taomlar" 2-qavat.

<b>🗺 Geolokatsiya:</b> https://t.me/Fitrat_study_kesh01/16
"""
}



@router.message(CommandStart(), IsRegisteredUser())
async def start(message: Message):  
    await message.answer("Sizni yana ko‘rib turganimdan hursandman!", reply_markup=main_menu_users_btn(is_registered=True))

@router.message(F.text == "Vakansiyalar", IsRegisteredUser())
async def vacancies(message: Message):  
    await message.answer("Vakansiya turini tanlang.", reply_markup=vacancies_btn)

@router.message(F.text == "Biz haqimizda")
async def about(message: Message):  
    await message.bot.copy_message(chat_id=message.chat.id, from_chat_id=-1003848271662, message_id=7, parse_mode="HTML", reply_markup=branches_btn())

@router.callback_query(F.data.startswith("branch_"))
async def branch_callback(callback: CallbackQuery):
    branch = callback.data.split("_")[1]
    try:
        await callback.message.edit_caption(caption=branches_text.get(branch, f"filial: {branch}"), parse_mode="HTML", reply_markup=branches_btn(selected_branch=branch))
    finally:
        await callback.answer()

@router.message(F.text == "Bog‘lanish")
async def contact(message: Message):  
    await message.answer(
        "📞 <b>Biz bilan bog’lanish</b>\n\n"
        "👤 <b>Rekruter:</b> +998973729000\n\n"
        "🏢 <b>Yangihayot filiali (Call-markaz):</b> +998910899000",
        parse_mode="HTML"
    )

@router.message(F.text == "Orqaga")
async def back(message: Message, state: FSMContext):
    exists = await TgUser.get_or_none(tg_id=message.chat.id)
    if exists:
        await message.answer("Orqaga qaytdik!!", reply_markup=main_menu_users_btn(is_registered=True))
    else:
        await message.answer("Orqaga qaytdik!!", reply_markup=main_menu_users_btn(is_registered=False))
    await state.clear()
