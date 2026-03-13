from database.models import Subjects
from aiogram import Router, F, Bot
from aiogram.types import Message
from keyboards.reply import admin_menu, kasblar_lst_btn, back_btn, admin_kasb_detail_btn
from states.admin import AdminKasbStates
from aiogram.fsm.context import FSMContext
from database.models import VacanciesText, Subjects
from filters.admin import InKasblarStateGroup, IsAdmin

router = Router()

@router.message(F.text == "Orqaga", InKasblarStateGroup())
async def f(message: Message, state: FSMContext):
    match await state.get_state():
        case AdminKasbStates.select_kasb:
            await state.clear()
            await message.answer("Bosh menyu", reply_markup=admin_menu)
        case AdminKasbStates.add_kasb:
            await select_kasb_menu(message, state)
        case AdminKasbStates.add_kasb_text:
            await state.set_state(AdminKasbStates.add_kasb)
            await message.answer("Kasb nomini kiriting.", reply_markup=back_btn)
        case AdminKasbStates.about_kasb:
            ignor_names = [sub.name for sub in await Subjects.all()]
            await state.set_state(AdminKasbStates.select_kasb)
            await message.answer("Kasblardan birini tanlang yoki yangisini qo‘shing.", reply_markup=kasblar_lst_btn([sub.name for sub in await VacanciesText.exclude(name__in=ignor_names).all()], is_admin=True))
        case AdminKasbStates.update_vacancy_text:
            await state.set_state(AdminKasbStates.about_kasb)
            state_data = await state.get_data()
            vacancy_text = await VacanciesText.get_or_none(id=state_data["vacancy_text_id"])
            if vacancy_text:
                await message.answer(vacancy_text.text, reply_markup=admin_kasb_detail_btn())
            else:
                await message.answer("Bunday kasb mavjud emas!")
                await state.set_state(AdminKasbStates.select_kasb)
                await message.answer("Kasblardan birini tanlang yoki yangisini qo‘shing.", reply_markup=kasblar_lst_btn([sub.name for sub in await VacanciesText.exclude(name__in=ignor_names).all()], is_admin=True))

@router.message(F.text == "Kasblar", IsAdmin())
async def select_kasb_menu(message: Message, state: FSMContext):
    ignor_names = [sub.name for sub in await Subjects.all()]
    await state.set_state(AdminKasbStates.select_kasb)
    await message.answer("Kasblardan birini tanlang yoki yangisini qo‘shing.", reply_markup=kasblar_lst_btn([sub.name for sub in await VacanciesText.exclude(name__in=ignor_names).all()], is_admin=True))

@router.message(F.text == "Yangi kasb qo‘shish", AdminKasbStates.select_kasb)
async def add_kasb(message: Message, state: FSMContext):
    await state.set_state(AdminKasbStates.add_kasb)
    await message.answer("Kasb nomini kiriting.", reply_markup=back_btn)

@router.message(F.text, AdminKasbStates.add_kasb)
async def add_kasb_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Kasb matnini yuboring.", reply_markup=back_btn)
    await state.set_state(AdminKasbStates.add_kasb_text)

@router.message(F.text, AdminKasbStates.add_kasb_text)
async def add_kasb_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    state_data = await state.get_data()
    await VacanciesText.create(name=state_data["name"], text=state_data["text"])
    await message.answer("Kasb qo‘shildi.", reply_markup=kasblar_lst_btn([sub.name for sub in await VacanciesText.all()], is_admin=True))
    await state.set_state(AdminKasbStates.select_kasb)

@router.message(F.text, AdminKasbStates.select_kasb)
async def select_kasb(message: Message, state: FSMContext):
    vacancy_text = await VacanciesText.get_or_none(name=message.text)
    if not vacancy_text:
        await message.answer("Bunday kasb mavjud emas!")
        return
    await state.update_data(vacancy_text_id=vacancy_text.id)
    await message.answer(vacancy_text.text, reply_markup=admin_kasb_detail_btn())
    await state.set_state(AdminKasbStates.about_kasb)

@router.message(F.text == "Kasbni o‘chirish", AdminKasbStates.about_kasb)
async def delete_kasb(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await VacanciesText.filter(id=state_data["vacancy_text_id"]).delete()
    await message.answer("Kasb o‘chirildi.", reply_markup=kasblar_lst_btn([sub.name for sub in await VacanciesText.all()], is_admin=True))
    await state.set_state(AdminKasbStates.select_kasb)

@router.message(F.text == "Vakansiya matnini yangilash", AdminKasbStates.about_kasb)
async def update_vacancy_text(message: Message, state: FSMContext):
    await state.set_state(AdminKasbStates.update_vacancy_text)
    await message.answer("Vakansiya matnini yuboring.", reply_markup=back_btn)

@router.message(F.text, AdminKasbStates.update_vacancy_text)
async def update_vacancy_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    vacancy_text = await VacanciesText.get_or_none(id=state_data["vacancy_text_id"])
    if vacancy_text:
        vacancy_text.text = message.text
        await vacancy_text.save()
        await message.answer("Vakansiya matni yangilandi.", reply_markup=admin_kasb_detail_btn())
        await state.set_state(AdminKasbStates.about_kasb)
    else:
        await message.answer("Bunday kasb mavjud emas!")
        await state.set_state(AdminKasbStates.select_kasb)
        await message.answer("Kasblardan birini tanlang yoki yangisini qo‘shing.", reply_markup=kasblar_lst_btn([sub.name for sub in await VacanciesText.all()], is_admin=True))

@router.message(F.text == "Oxirgi matnni yangilash", AdminKasbStates.about_kasb)
async def update_last_text(message: Message, state: FSMContext):
    await state.set_state(AdminKasbStates.update_last_text)
    await message.answer("Oxirgi matnni yuboring.", reply_markup=back_btn)

@router.message(F.text, AdminKasbStates.update_last_text)
async def update_last_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    vacancy_text = await VacanciesText.get_or_none(id=state_data["vacancy_text_id"])
    if vacancy_text:
        vacancy_text.last_text = message.text
        await vacancy_text.save()
        await message.answer("Oxirgi matn yangilandi.", reply_markup=admin_kasb_detail_btn())
        await state.set_state(AdminKasbStates.about_kasb)
    else:
        await message.answer("Bunday kasb mavjud emas!")
        await state.set_state(AdminKasbStates.select_kasb)
        await message.answer("Kasblardan birini tanlang yoki yangisini qo‘shing.", reply_markup=kasblar_lst_btn([sub.name for sub in await VacanciesText.all()], is_admin=True))
