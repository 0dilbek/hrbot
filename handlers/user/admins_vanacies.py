from aiogram import Router, F
from aiogram.types import Message
from filters.user import IsRegisteredUser
from aiogram.fsm.context import FSMContext
from keyboards.reply import (
    kasblar_lst_btn,
    working_time_btn,
    back_btn,
    main_menu_users_btn,
    vacancies_btn,
    confirm_btn,
    experience_btn,
)
from database.models import VacanciesText, Subjects, AdminsResume, TgUser, VacanciesText
from states.user import AdminsVacancyState
from config import ADMINS
from filters.user import InAdminsResumeState
from utils import is_valid_phone

router = Router()


@router.message(F.text == "Orqaga", InAdminsResumeState())
async def admins_vanacies(message: Message, state: FSMContext):
    state_data = await state.get_data()
    match await state.get_state():
        case AdminsVacancyState.vacancy_type:
            await message.answer("Ortga qaytildi.", reply_markup=vacancies_btn)
            await state.clear()
            return
        case AdminsVacancyState.working_time:
            await admins_vanacies_start(message, state)
        case AdminsVacancyState.foreign_language:
            await message.answer("Ish vaqtini tanlang:", reply_markup=working_time_btn)
            await state.set_state(AdminsVacancyState.working_time)
        case AdminsVacancyState.foreign_language_level:
            await message.answer(
                "Qaysi xorijiy tillarni bilasiz?", reply_markup=back_btn
            )
            await state.set_state(AdminsVacancyState.foreign_language)
        case AdminsVacancyState.experience:
            await admins_vanacies_foreign_language(message, state)
        case AdminsVacancyState.last_work_place:
            await admins_vanacies_foreign_language_level(message, state)
        case AdminsVacancyState.why_leave_work:
            await admins_vanacies_experience(message, state)
        case AdminsVacancyState.last_work_place_phone:
            await admins_vanacies_last_work_place(message, state)
        case AdminsVacancyState.why_choice_us:
            if state_data.get("experience") == "Hech qayerda ishlamaganman":
                await message.answer(
                    "Sohadagi tajribangiz necha yil?", reply_markup=experience_btn
                )
                await state.set_state(AdminsVacancyState.experience)
            else:
                await message.answer(
                    "Oxirgi ish joyingiz telefon raqami?", reply_markup=back_btn
                )
                await state.set_state(AdminsVacancyState.last_work_place_phone)
        case AdminsVacancyState.confirm:
            await message.answer("Nega aynan bizni tanladingiz?", reply_markup=back_btn)
            await state.set_state(AdminsVacancyState.why_choice_us)


@router.message(F.text == "Adminlarga", IsRegisteredUser())
async def admins_vanacies_start(message: Message, state: FSMContext):
    kasblar = await VacanciesText.exclude(
        name__in=[sub.name for sub in await Subjects.all()]
    )
    if not kasblar:
        await message.answer("Hozirda adminlarga vakansiya mavjud emas!")
        return

    await message.answer(
        "Vakansiyani tanlang:",
        reply_markup=kasblar_lst_btn(
            kasblar=[kasb.name for kasb in kasblar], is_admin=False
        ),
    )
    await state.set_state(AdminsVacancyState.vacancy_type)


@router.message(F.text, AdminsVacancyState.vacancy_type)
async def admins_vanacies_vacancy_type(message: Message, state: FSMContext):
    if message.text not in [
        kasb.name
        for kasb in await VacanciesText.exclude(
            name__in=[sub.name for sub in await Subjects.all()]
        )
    ]:
        await message.answer("Bunday vakansiya mavjud emas!")
        return
    await state.update_data(vacancy_type=message.text)
    vacansy_text = await VacanciesText.get_or_none(name=message.text)
    if vacansy_text.text.strip():
        await message.answer(vacansy_text.text, parse_mode="HTML")
    await message.answer("Ish vaqtini tanlang:", reply_markup=working_time_btn)
    await state.set_state(AdminsVacancyState.working_time)


@router.message(F.text, AdminsVacancyState.working_time)
async def admins_vanacies_working_time(message: Message, state: FSMContext):
    if message.text in [
        "09:00 - 20:00",
        "08:00 - 17:00",
        "14:00 - 20:00",
        "08:00 - 20:00",
    ]:
        await state.update_data(working_time=message.text)
        await message.answer("Qaysi xorijiy tilni bilasiz?", reply_markup=back_btn)
        await state.set_state(AdminsVacancyState.foreign_language)
    else:
        await message.answer("Bunday ish vaqti mavjud emas!")


@router.message(F.text, AdminsVacancyState.foreign_language)
async def admins_vanacies_foreign_language(message: Message, state: FSMContext):
    await state.update_data(foreign_language=message.text)
    await message.answer(
        "Xorijiy tilni bilish darajangizni kiriting.", reply_markup=back_btn
    )
    await state.set_state(AdminsVacancyState.foreign_language_level)


@router.message(F.text, AdminsVacancyState.foreign_language_level)
async def admins_vanacies_foreign_language_level(message: Message, state: FSMContext):
    state_data = await state.get_data()
    foreign_languages = state_data.get("foreign_languages", [])
    foreign_languages.append(
        {"language": state_data.get("foreign_language", ""), "level": message.text}
    )
    await state.update_data(foreign_languages=foreign_languages)

    await message.answer("Yana xorijiy til bilasizmi?", reply_markup=confirm_btn)
    await state.set_state(AdminsVacancyState.continue_foreign_language)


@router.message(F.text, AdminsVacancyState.continue_foreign_language)
async def admins_vanacies_continue_foreign_language(
    message: Message, state: FSMContext
):
    if message.text == "Ha":
        await message.answer("Yana qaysi xorijiy tilni bilasiz?", reply_markup=back_btn)
        await state.set_state(AdminsVacancyState.foreign_language)
    elif message.text == "Yo‘q":
        await message.answer(
            "Sohadagi tajribangiz necha yil?", reply_markup=experience_btn
        )
        await state.set_state(AdminsVacancyState.experience)
    else:
        await message.answer("Iltimos, 'Ha' yoki 'Yo‘q' tanlang!")


@router.message(F.text, AdminsVacancyState.experience)
async def admins_vanacies_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    if message.text == "Hech qayerda ishlamaganman":
        await message.answer("Nega aynan bizni tanladingiz?", reply_markup=back_btn)
        await state.set_state(AdminsVacancyState.why_choice_us)
        return
    await message.answer("Oxirgi ish joyingiz qayer edi?", reply_markup=back_btn)
    await state.set_state(AdminsVacancyState.last_work_place)


@router.message(F.text, AdminsVacancyState.last_work_place)
async def admins_vanacies_last_work_place(message: Message, state: FSMContext):
    await state.update_data(last_work_place=message.text)
    await message.answer(
        "Oxirgi ish joyingizdan ketish sababini kiriting", reply_markup=back_btn
    )
    await state.set_state(AdminsVacancyState.why_leave_work)


@router.message(F.text, AdminsVacancyState.why_leave_work)
async def admins_vanacies_why_leave_work(message: Message, state: FSMContext):
    await state.update_data(why_leave_work=message.text)
    await message.answer(
        "Oxirgi ishlagan tashkilotingiz yoki to‘g‘ridan-to‘g‘ri rahbaringiz telefon raqamini qoldiring.\n\nMasalan: +998901234567",
        reply_markup=back_btn,
    )
    await state.set_state(AdminsVacancyState.last_work_place_phone)


@router.message(F.text, AdminsVacancyState.last_work_place_phone)
async def admins_vanacies_last_work_place_phone(message: Message, state: FSMContext):
    if is_valid_phone(message.text):
        await state.update_data(last_work_place_phone=message.text)
        await message.answer("Nega aynan bizni tanladingiz?", reply_markup=back_btn)
        await state.set_state(AdminsVacancyState.why_choice_us)
    else:
        await message.answer(
            "Noto‘g‘ri telefon raqam! To‘g‘ri telefon raqam kiriting.\n\nMasalan, +998901234567"
        )


@router.message(F.text, AdminsVacancyState.why_choice_us)
async def admins_vanacies_why_choice_us(message: Message, state: FSMContext):
    state_data = await state.get_data()
    foreigin_languages_text = "\n\n"
    if state_data.get("foreign_languages"):
        for lang in state_data["foreign_languages"]:
            foreigin_languages_text += f"\t\t• {lang['language']} - {lang['level']}\n"
        foreigin_languages_text += "\n"
    else:
        foreigin_languages_text = "Yo'q"

    await message.answer(
        f"""
Ma’lumotlaringiz:

Kasb: {state_data["vacancy_type"]}
Ish vaqti: {state_data["working_time"]}
Xorijiy til: {foreigin_languages_text}
Tajriba: {state_data["experience"]}
Oxirgi ish joyi: {state_data.get('last_work_place', "yo‘q")}
Oxirgi ish joyidan ketish sababi: {state_data.get('why_leave_work', "yo‘q")}
Oxirgi ish joyi telefon raqami: {state_data.get('last_work_place_phone', "yo‘q")}
Nega aynan bizni tanladingiz?: {message.text}

Ma’lumotlaringiz to‘g‘riligini tasdiqlang.
    """,
        reply_markup=confirm_btn,
    )
    await state.update_data(why_choice_us=message.text)
    await state.set_state(AdminsVacancyState.confirm)


@router.message(AdminsVacancyState.confirm)
async def confirm(message: Message, state: FSMContext):
    if message.text.lower() == "ha":
        state_data = await state.get_data()
        user = await TgUser.get_or_none(tg_id=message.from_user.id)
        await AdminsResume.create(
            user=user,
            job=state_data["vacancy_type"],
            working_time=state_data["working_time"],
            foreign_languages=state_data["foreign_languages"],
            experience=state_data["experience"],
            last_work_place=state_data.get("last_work_place", "yo‘q"),
            why_leave_work=state_data.get("why_leave_work", "yo‘q"),
            last_work_place_phone=state_data.get("last_work_place_phone", "yo‘q"),
            why_choice_us=state_data.get("why_choice_us"),
        )
        foreigin_languages_text = "\n\n"
        if state_data.get("foreign_languages"):
            for lang in state_data["foreign_languages"]:
                foreigin_languages_text += (
                    f"\t\t• {lang['language']} - {lang['level']}\n"
                )
        else:
            foreigin_languages_text = "Yo‘q"

        phones_text = "\n\n"
        for phone in user.phone_numbers:
            phones_text += f"\t\t• {user.phone_numbers[phone]}\n"
        phones_text += "\n"

        caption = f"""
Yangi rezyume qo‘shildi:

<blockquote expandable>
Ism-Familiya: {user.full_name}
Filial: {user.branch if user.branch else "Yo'q"}
Telefon raqamlar: {phones_text}
Kasb: {state_data["vacancy_type"]}
Ish vaqti: {state_data["working_time"]}
Xorijiy til: {foreigin_languages_text}
Tajriba: {state_data["experience"]}
Oxirgi ish joyi: {state_data.get("last_work_place", "yo‘q")}
Oxirgi ish joyidan ketish sababi: {state_data.get("why_leave_work", "yo‘q")}
Oxirgi ish joyi telefon raqami: {state_data.get("last_work_place_phone", "yo‘q")}
Nega aynan bizni tanladingiz?: {state_data.get("why_choice_us")}
</blockquote>
            """
        for admin in ADMINS:
            try:
                if user.profile_pic_file_id:
                    await message.bot.send_photo(
                        chat_id=admin,
                        photo=user.profile_pic_file_id,
                        caption=caption,
                        parse_mode="HTML",
                    )
                else:
                    await message.bot.send_message(
                        chat_id=admin, text=caption, parse_mode="HTML"
                    )
            except Exception as e:
                print(e)
        vacancy_text = await VacanciesText.get_or_none(name=state_data["vacancy_type"])
        if vacancy_text and len(vacancy_text.last_text.strip()) > 5:
            await message.answer(
                vacancy_text.last_text,
                parse_mode="HTML",
                reply_markup=main_menu_users_btn(is_registered=True),
            )
        else:
            await message.answer(
                """
Sabr bilan shu joyigacha kelganingiz uchun raxmat! Siz birinchi bosqichdan muvaffaqiyatli o‘tdingiz!

Tez orada siz bilan bog‘lanamiz!
        """,
                reply_markup=main_menu_users_btn(is_registered=True),
            )
        await state.clear()
    else:
        await message.answer(
            "Ma‘lumotlarni yuborish bekor qilindi!",
            reply_markup=main_menu_users_btn(is_registered=True),
        )
        await state.clear()
