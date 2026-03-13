from aiogram import Router, F, Bot
from aiogram.types import Message, FSInputFile
from keyboards.reply import admin_menu, fanlar_lst_btn, sertifikatlar_lst_btn, sertifikat_balls_lst_btn, back_btn
from states.admin import AdminSubjectStates
from aiogram.fsm.context import FSMContext
from database.models import Subjects, Sertificates, Quizs, VacanciesText
from filters.admin import InFanlarStateGroup, IsAdmin
from utils.fanlar import get_test_questions

router = Router()

@router.message(F.text == "Orqaga", InFanlarStateGroup(), IsAdmin())
async def ortga(message: Message, state: FSMContext):
    state_data = await state.get_data()
    match await state.get_state():
        case AdminSubjectStates.select_fan:
            await state.clear()
            await message.answer("Ortga qaytildi!", reply_markup=admin_menu)
        case AdminSubjectStates.add_fan:
            await state.set_state(AdminSubjectStates.select_fan)
            await message.answer("Ortga qaytildi!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        case AdminSubjectStates.add_sertifikat:
            await state.set_state(AdminSubjectStates.select_sertifikat)
            subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
            if not subject:
                await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
                await state.set_state(AdminSubjectStates.select_fan)
                return
            await message.answer("Ortga qaytildi!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        case AdminSubjectStates.add_sertifikat_balls:
            await state.set_state(AdminSubjectStates.select_sertifikat)
            await message.answer("Sertifikat nom!ni kiriting", reply_markup=back_btn)
        case AdminSubjectStates.select_sertifikat:
            await state.set_state(AdminSubjectStates.select_fan)
            await message.answer("Ortga qaytildi!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        case AdminSubjectStates.view_balls:
            await state.set_state(AdminSubjectStates.select_sertifikat)
            subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
            if not subject:
                await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
                await state.set_state(AdminSubjectStates.select_fan)
                return
            await message.answer("Ortga qaytildi!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        case AdminSubjectStates.add_ball:
            await state.set_state(AdminSubjectStates.view_balls)
            sertificate = await Sertificates.get_or_none(id=state_data['selected_sertificate_id'])
            if not sertificate:
                subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
                if not subject:
                    await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
                    await state.set_state(AdminSubjectStates.select_fan)
                    return
                await message.answer("Bunday sertifikat mavjud emas!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
                await state.set_state(AdminSubjectStates.select_sertifikat)
                return
            await message.answer("Ortga qaytildi!", reply_markup=sertifikat_balls_lst_btn(sertificate.ball_list, is_admin=True, is_new=False))
        case AdminSubjectStates.delete_ball:
            await state.set_state(AdminSubjectStates.view_balls)
            sertificate = await Sertificates.get_or_none(id=state_data['selected_sertificate_id'])
            if not sertificate:
                subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
                if not subject:
                    await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
                    await state.set_state(AdminSubjectStates.select_fan)
                    return
                await message.answer("Bunday sertifikat mavjud emas!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
                await state.set_state(AdminSubjectStates.select_sertifikat)
                return
            await message.answer("Ortga qaytildi!", reply_markup=sertifikat_balls_lst_btn(sertificate.ball_list, is_admin=True, is_new=False))
        case AdminSubjectStates.update_quiz:
            await state.set_state(AdminSubjectStates.select_sertifikat)
            subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
            if not subject:
                await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
                await state.set_state(AdminSubjectStates.select_fan)
                return
            await message.answer("Ortga qaytildi!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        case AdminSubjectStates.update_vacancy_text:
            await state.set_state(AdminSubjectStates.select_sertifikat)
            subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
            if not subject:
                await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
                await state.set_state(AdminSubjectStates.select_fan)
                return
            await message.answer("Ortga qaytildi!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))


@router.message(F.text == "Fanlar", IsAdmin())
async def fanlar(message: Message, state: FSMContext):
    await state.set_state(AdminSubjectStates.select_fan)
    await message.answer("Fanlardan birini tanlang yoki yangisini qo‘shing.", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))

@router.message(F.text == "Yangi fan qo‘shish", AdminSubjectStates.select_fan, IsAdmin())
async def add_fan(message: Message, state: FSMContext):
    await state.set_state(AdminSubjectStates.add_fan)
    await message.answer("Yangi fan nomini kiriting.", reply_markup=back_btn)

@router.message(F.text, AdminSubjectStates.add_fan)
async def add_fan(message: Message, state: FSMContext):
    exists = await Subjects.filter(name=message.text).exists()
    if exists:  
        await message.answer("Bunday fan mavjud!")
        return
    await Subjects.create(name=message.text)
    await state.set_state(AdminSubjectStates.select_fan)
    await message.answer("Yangi fan qo‘shildi!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))

@router.message(F.text, AdminSubjectStates.select_fan, IsAdmin())
async def select_fan(message: Message, state: FSMContext):
    subject = await Subjects.get(name=message.text)
    await state.update_data(selected_subject_id=subject.id)
    await message.answer("Fan tanlandi!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
    await state.set_state(AdminSubjectStates.select_sertifikat)


@router.message(F.text == "Test faylini yangilash", AdminSubjectStates.select_sertifikat)
async def update_test_file(message: Message, state: FSMContext):
    await state.set_state(AdminSubjectStates.update_quiz)
    await message.answer("Test faylini yuklang", reply_markup=back_btn)

@router.message(F.text == "Shablon faylni olish", AdminSubjectStates.select_sertifikat)
async def get_template_file(message: Message, state: FSMContext):
    await message.answer_document(document=FSInputFile("template.xlsx"))

@router.message(AdminSubjectStates.update_quiz)
async def update_test_file(message: Message, state: FSMContext, bot: Bot):
    if not message.document:
        await message.answer("Iltimos, testni fayl ko‘rinishida yuboring.")
        return
    if not message.document.file_name.endswith(".xlsx"):
        await message.answer("Iltimos, testni .xlsx formatida yuboring.")
        return
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!")
        await state.set_state(AdminSubjectStates.select_fan)
        await message.answer("Fanlardan birini tanlang yoki yangisini qo‘shing.", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        return
    file_path = f"statics/tests/{subject.name}.xlsx"

    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, file_path)

    try:
        questions = await get_test_questions(file_path)
    except ValueError as e:
        await message.answer(f"Xatolik:Iltimos, faylni tekshirib qayta yuboring.")
        return
    except Exception as e:
        await message.answer(f"Kutilmagan xatolik: {str(e)}")
        return

    await Quizs.filter(subject=subject).delete()
    await Quizs.create(
        subject=subject,
        quizs=questions
    )
    await message.answer(f"Test fayli yangilandi!\n\nJami {len(questions)} ta savol bazaga yuklandi.", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
    await state.set_state(AdminSubjectStates.select_sertifikat)

@router.message(F.text == "Yangi sertifikat qo‘shish", AdminSubjectStates.select_sertifikat)
async def add_sertifikat(message: Message, state: FSMContext):
    await state.set_state(AdminSubjectStates.add_sertifikat)
    await message.answer("Yangi sertifikat nomini kiriting.", reply_markup=back_btn)

@router.message(F.text == "Fanni o‘chirish", AdminSubjectStates.select_sertifikat)
async def delete_fan(message: Message, state: FSMContext):
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!")
        await state.set_state(AdminSubjectStates.select_fan)
        await message.answer("Fanlardan birini tanlang yoki yangisini qo‘shing.", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        return
    await subject.delete()
    await state.set_state(AdminSubjectStates.select_fan)
    await message.answer("Fan o‘chirildi!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))

@router.message(F.text == "Vakansiya matnini yangilash", AdminSubjectStates.select_sertifikat)
async def update_vacancy_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!")
        await state.set_state(AdminSubjectStates.select_fan)
        await message.answer("Fanlardan birini tanlang yoki yangisini qo‘shing.", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        return
    vacancy = await VacanciesText.filter(name=subject.name).first()
    if vacancy.text:
        await state.update_data(selected_vacancy_id=vacancy.id)
        await message.answer(vacancy.text)
    await state.set_state(AdminSubjectStates.update_vacancy_text)
    await message.answer("Vakansiya matnini kiriting.", reply_markup=back_btn)

@router.message(F.text, AdminSubjectStates.update_vacancy_text)
async def update_vacancy_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!")
        await state.set_state(AdminSubjectStates.select_fan)
        await message.answer("Fanlardan birini tanlang yoki yangisini qo‘shing.", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        return
    vacancy = await VacanciesText.filter(name=subject.name).first()
    if not vacancy:
        await VacanciesText.create(name=subject.name, text=message.text)
    else:
        vacancy.text = message.text
        await vacancy.save()
    await state.set_state(AdminSubjectStates.select_sertifikat)
    await message.answer("Vakansiya matni yangilandi!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))

@router.message(F.text == "Oxirgi matnni yangilash", AdminSubjectStates.select_sertifikat)
async def update_last_text(message: Message, state: FSMContext):
    await state.set_state(AdminSubjectStates.update_last_text)
    await message.answer("Oxirgi matnni yuboring.", reply_markup=back_btn)

@router.message(F.text, AdminSubjectStates.update_last_text)
async def update_last_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!")
        await state.set_state(AdminSubjectStates.select_fan)
        await message.answer("Fanlardan birini tanlang yoki yangisini qo‘shing.", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        return
    vacancy = await VacanciesText.filter(name=subject.name).first()
    if not vacancy:
        await VacanciesText.create(name=subject.name, text="", last_text=message.text)
    else:
        vacancy.last_text = message.text
        await vacancy.save()
    await state.set_state(AdminSubjectStates.select_sertifikat)
    await message.answer("Oxirgi matn yangilandi!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))

@router.message(F.text, AdminSubjectStates.add_sertifikat)
async def add_sertifikat(message: Message, state: FSMContext):
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!")
        await state.set_state(AdminSubjectStates.select_fan)
        await message.answer("Fanlardan birini tanlang yoki yangisini qo‘shing.", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        return
    exists = await Sertificates.filter(name=message.text, subject=subject).exists()
    if exists:
        await message.answer("Bunday sertifikat mavjud!")
        return
    sertificate = await Sertificates.create(name=message.text, subject=subject)
    await state.update_data(selected_sertificate_id=sertificate.id)
    await message.answer("Tanlanadigan ballarni kiriting.", reply_markup=sertifikat_balls_lst_btn([], is_admin=True, is_new=True))
    await state.set_state(AdminSubjectStates.add_sertifikat_balls)

@router.message(F.text == "Tugadi", AdminSubjectStates.add_sertifikat_balls)
async def add_sertifikat_balls(message: Message, state: FSMContext):
    state_data = await state.get_data()
    sertificate = await Sertificates.get_or_none(id=state_data['selected_sertificate_id'])
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!")
        await state.set_state(AdminSubjectStates.select_fan)
        await message.answer("Fanlardan birini tanlang yoki yangisini qo‘shing.", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        return
    if not sertificate:
        await message.answer("Bunday sertifikat mavjud emas!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        await state.set_state(AdminSubjectStates.select_sertifikat)
        return
    if not sertificate.ball_list:
        await message.answer("Bu sertifikatga hali ball qo‘shilmadi!")
        return
    await message.answer(f"\"{sertificate.name}\" sertifikatiga ballar qo‘shildi!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
    await state.set_state(AdminSubjectStates.select_sertifikat)

@router.message(F.text, AdminSubjectStates.add_sertifikat_balls)
async def add_sertifikat_balls(message: Message, state: FSMContext):
    state_data = await state.get_data()
    sertificate = await Sertificates.get_or_none(id=state_data['selected_sertificate_id'])
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!")
        await state.set_state(AdminSubjectStates.select_fan)
        await message.answer("Fanlardan birini tanlang yoki yangisini qo‘shing.", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        return
    if not sertificate:
        await message.answer("Bunday sertifikat mavjud emas!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        await state.set_state(AdminSubjectStates.select_sertifikat)
        return
    if message.text in sertificate.ball_list:
        await message.answer("Bunday ball mavjud!")
        return
    sertificate.ball_list.append(message.text)
    await sertificate.save()
    await message.answer("Sertifikatga ball qo‘shildi!", reply_markup=sertifikat_balls_lst_btn(sertificate.ball_list, is_admin=True, is_new=True))
    await state.set_state(AdminSubjectStates.add_sertifikat_balls)

@router.message(F.text, AdminSubjectStates.select_sertifikat)
async def select_sertifikat(message: Message, state: FSMContext):
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        await state.set_state(AdminSubjectStates.select_fan)
        return
    sertificate = await Sertificates.get_or_none(name=message.text, subject=subject)
    if not sertificate:
        await message.answer("Bunday sertifikat mavjud emas!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        await state.set_state(AdminSubjectStates.select_sertifikat)
        return
    await state.update_data(selected_sertificate_id=sertificate.id)
    await message.answer("Sertifikat tanlandi!", reply_markup=sertifikat_balls_lst_btn(sertificate.ball_list, is_admin=True, is_new=False))
    await state.set_state(AdminSubjectStates.view_balls)

@router.message(F.text == "Ball qo‘shish", AdminSubjectStates.view_balls)
async def add_ball(message: Message, state: FSMContext):
    await state.set_state(AdminSubjectStates.add_ball)
    await message.answer("Ballni kiriting", reply_markup=back_btn)

@router.message(F.text == "Sertifikatni o‘chirish", AdminSubjectStates.view_balls)
async def delete_sertificate(message: Message, state: FSMContext):
    state_data = await state.get_data()
    sertificate = await Sertificates.get_or_none(id=state_data['selected_sertificate_id'])
    subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
    if not subject:
        await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
        await state.set_state(AdminSubjectStates.select_fan)
        return
    if not sertificate:
        await message.answer("Bunday sertifikat mavjud emas!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        await state.set_state(AdminSubjectStates.select_sertifikat)
        return
    await sertificate.delete()

    await state.set_state(AdminSubjectStates.select_sertifikat)
    await message.answer("Sertifikat o‘chirildi!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))

@router.message(F.text, AdminSubjectStates.add_ball)
async def add_ball(message: Message, state: FSMContext):
    state_data = await state.get_data()
    sertificate = await Sertificates.get_or_none(id=state_data['selected_sertificate_id'])
    if not sertificate:
        subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
        if not subject:
            await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
            await state.set_state(AdminSubjectStates.select_fan)
            return
        await message.answer("Bunday sertifikat mavjud emas!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        await state.set_state(AdminSubjectStates.select_sertifikat)
        return
    if message.text in sertificate.ball_list:
        await message.answer("Bunday ball mavjud!")
        return
    sertificate.ball_list.append(message.text)
    await sertificate.save()
    await message.answer("Ball qo‘shildi!", reply_markup=sertifikat_balls_lst_btn(sertificate.ball_list, is_admin=True, is_new=False))
    await state.set_state(AdminSubjectStates.view_balls)

@router.message(F.text == "Ball o‘chirish", AdminSubjectStates.view_balls)
async def delete_ball(message: Message, state: FSMContext):
    await state.set_state(AdminSubjectStates.delete_ball)
    state_data = await state.get_data()
    sertificate = await Sertificates.get_or_none(id=state_data['selected_sertificate_id'])
    if not sertificate:
        subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
        if not subject:
            await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
            await state.set_state(AdminSubjectStates.select_fan)
            return
        await message.answer("Bunday sertifikat mavjud emas!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        await state.set_state(AdminSubjectStates.select_sertifikat)
        return
    await message.answer("O‘chiriladigan ballni tanlang", reply_markup=sertifikat_balls_lst_btn(sertificate.ball_list, is_admin=False, is_new=False))

@router.message(F.text, AdminSubjectStates.delete_ball)
async def delete_ball(message: Message, state: FSMContext):
    state_data = await state.get_data()
    sertificate = await Sertificates.get_or_none(id=state_data['selected_sertificate_id'])
    if not sertificate:
        subject = await Subjects.get_or_none(id=state_data['selected_subject_id'])
        if not subject:
            await message.answer("Bunday fan mavjud emas!", reply_markup=fanlar_lst_btn([sub.name for sub in await Subjects.all()], is_admin=True))
            await state.set_state(AdminSubjectStates.select_fan)
            return
        await message.answer("Bunday sertifikat mavjud emas!", reply_markup=sertifikatlar_lst_btn([s.name for s in await Sertificates.filter(subject=subject)], is_admin=True))
        await state.set_state(AdminSubjectStates.select_sertifikat)
        return
    try:
        sertificate.ball_list.remove(message.text)
    except ValueError:
        await message.answer("Bunday ball mavjud emas!")
        return
    await sertificate.save()
    await message.answer("Ball o‘chirildi!", reply_markup=sertifikat_balls_lst_btn(sertificate.ball_list, is_admin=True, is_new=False))
    await state.set_state(AdminSubjectStates.view_balls)

