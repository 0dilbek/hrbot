from aiogram.types import ReplyKeyboardRemove
from aiogram import Router, F, Bot
from aiogram.types import (
    Message,
    PollAnswer,
    ReplyKeyboardRemove,
    CallbackQuery,
)
from filters.user import IsRegisteredUser
from keyboards.reply import (
    vacancies_btn,
    fanlar_lst_btn,
    working_time_btn,
    confirm_btn,
    sertifikatlar_lst_btn,
    sertifikat_balls_lst_btn,
    back_btn,
    main_menu_users_btn,
    ready_btn,
    experience_btn,
)
from keyboards.inline import teacher_position_btn
from database.models import (
    Subjects,
    Sertificates,
    TeacherResume,
    TgUser,
    Quizs,
    QuizAnswers,
    VacanciesText,
)
from aiogram.fsm.context import FSMContext
from states.user import TeachersVacancyState
from filters.user import IsRegisteredUser, InTeachersResumeState
from datetime import datetime, timedelta, timezone
from config import ADMINS
from asyncio import sleep, create_task
from utils import is_valid_phone

router = Router()


@router.message(F.text == "Orqaga", InTeachersResumeState())
async def teachers_vacancy_back(message: Message, state: FSMContext):
    state_data = await state.get_data()
    match await state.get_state():
        case TeachersVacancyState.subject:
            await message.answer("orqaga qaytdik", reply_markup=vacancies_btn)
            await state.clear()
        case TeachersVacancyState.working_time:
            await message.answer(
                "Fanni tanlang.",
                reply_markup=fanlar_lst_btn(
                    [sub.name for sub in await Subjects.all()], False
                ),
            )
            await state.set_state(TeachersVacancyState.subject)
        case TeachersVacancyState.has_sertificate:
            if state_data.get("sertificates"):
                sertificates = state_data.get("sertificates")
                sertificates.pop()
                await state.update_data(sertificates=sertificates)
                await message.answer(
                    "Endi sertifikat faylini yuboring", reply_markup=back_btn
                )
                await state.set_state(TeachersVacancyState.sertificate_file)
            else:
                await message.answer(
                    "Ish vaqtini tanlang.", reply_markup=working_time_btn
                )
                await state.set_state(TeachersVacancyState.working_time)
        case TeachersVacancyState.sertificate_name:
            await message.answer(
                "Soha bo'yicha sertifikatingiz bormi?.", reply_markup=confirm_btn
            )
            await state.set_state(TeachersVacancyState.has_sertificate)
        case TeachersVacancyState.sertificate_ball:
            subject = await Subjects.get_or_none(id=state_data.get("subject_id"))
            if state_data.get("sertificates"):
                ignor_names = [ser["name"] for ser in state_data.get("sertificates")]
                await message.answer(
                    "Sertifikatingizni tanlang.",
                    reply_markup=sertifikatlar_lst_btn(
                        [
                            sert.name
                            for sert in await Sertificates.filter(
                                subject=subject
                            ).exclude(name__in=ignor_names)
                        ],
                        False,
                    ),
                )
                await state.set_state(TeachersVacancyState.sertificate_name)
            else:
                await message.answer(
                    "Sertifikatingizni tanlang.",
                    reply_markup=sertifikatlar_lst_btn(
                        [
                            sert.name
                            for sert in await Sertificates.filter(subject=subject)
                        ],
                        False,
                    ),
                )
                await state.set_state(TeachersVacancyState.sertificate_name)
        case TeachersVacancyState.sertificate_file:
            await message.answer(
                "Sertifikat bo‘yicha overall ballingizni tanlang.",
                reply_markup=sertifikat_balls_lst_btn(
                    [ball for ball in state_data.get("sertificate_ball_list")], False
                ),
            )
            await state.set_state(TeachersVacancyState.sertificate_ball)
        case TeachersVacancyState.position:
            await state.set_state(TeachersVacancyState.has_sertificate)
            await message.answer(
                "Yana sertifikatingiz bormi?", reply_markup=confirm_btn
            )
        case TeachersVacancyState.are_you_student:
            await state.set_state(TeachersVacancyState.position)
            await message.answer(
                "Ustozlar vakansiyasi bo‘yicha lavozimni tanlang.",
                reply_markup=teacher_position_btn,
            )
        case TeachersVacancyState.university:
            await state.set_state(TeachersVacancyState.are_you_student)
            await message.answer("Siz talabamisiz?", reply_markup=confirm_btn)
        case TeachersVacancyState.experience:
            if state_data.get("are_you_student") == "Ha":
                await message.answer(
                    "O’qiyotgan oliygohingiz, yo’nalishingiz va kursingizni kiriting?",
                    reply_markup=back_btn,
                )
                await state.set_state(TeachersVacancyState.university)
            else:
                await message.answer(
                    "Bitirgan oliygohingizni kiriting?", reply_markup=back_btn
                )
                await state.set_state(TeachersVacancyState.university)
        case TeachersVacancyState.last_work_place:
            await message.answer(
                "Sohadagi tajribangiz necha yil?", reply_markup=experience_btn
            )
            await state.set_state(TeachersVacancyState.experience)
        case TeachersVacancyState.why_leave_work:
            await message.answer(
                "Oxirgi ishlagan tashkilotingiz nomi?", reply_markup=back_btn
            )
            await state.set_state(TeachersVacancyState.last_work_place)
        case TeachersVacancyState.last_work_place_phone:
            await message.answer(
                "Oxirgi ish joyingizdan ketish sababini kiriting.",
                reply_markup=back_btn,
            )
            await state.set_state(TeachersVacancyState.why_leave_work)
        case TeachersVacancyState.salary:
            if state_data.get("experience") == "Hech qayerda ishlamaganman":
                await message.answer(
                    "Sohadagi tajribangiz necha yil?", reply_markup=experience_btn
                )
                await state.set_state(TeachersVacancyState.experience)
            else:
                await message.answer(
                    "Tashkilot telefon raqamini kiriting.", reply_markup=back_btn
                )
                await state.set_state(TeachersVacancyState.last_work_place_phone)
        case TeachersVacancyState.why_choice_us:
            await message.answer(
                "Bizdan qancha oylik maosh kutayapsiz?", reply_markup=back_btn
            )
            await state.set_state(TeachersVacancyState.salary)
        case TeachersVacancyState.confirm:
            await message.answer("Nega aynan bizni tanladingiz?", reply_markup=back_btn)
            await state.set_state(TeachersVacancyState.why_choice_us)
        case __:
            await message.answer(
                "Orqaga qaytildi!!",
                reply_markup=main_menu_users_btn(is_registered=True),
            )
            await state.clear()


@router.message(F.text == "Ustozlarga", IsRegisteredUser())
async def teachers_vacancy(message: Message, state: FSMContext):
    subjects = await Subjects.all()
    if not subjects:
        await message.answer("Hozirda hech qaysi fandan vakansiya mavjud emas!")
        return
    await message.answer(
        "Fanni tanlang.",
        reply_markup=fanlar_lst_btn([sub.name for sub in subjects], False),
    )
    await state.set_state(TeachersVacancyState.subject)


@router.message(F.text, TeachersVacancyState.subject)
async def select_subject(message: Message, state: FSMContext):
    subject = await Subjects.get_or_none(name=message.text)
    if not subject:
        await message.answer("Bunday fan mavjud emas!")
        return
    await state.update_data(subject_id=subject.id, subject_name=subject.name)
    await message.answer("Ish vaqtini tanlang.", reply_markup=working_time_btn)
    await state.set_state(TeachersVacancyState.working_time)


@router.message(F.text, TeachersVacancyState.working_time)
async def select_working_time(message: Message, state: FSMContext):
    if message.text in [
        "09:00 - 20:00",
        "08:00 - 17:00",
        "14:00 - 20:00",
        "08:00 - 20:00",
    ]:
        await state.update_data(working_time=message.text)
        await message.answer(
            "Soha bo'yicha sertifikatingiz bormi?.", reply_markup=confirm_btn
        )
        await state.set_state(TeachersVacancyState.has_sertificate)
    else:
        await message.answer("Bunday ish vaqti mavjud emas!")


@router.message(F.text, TeachersVacancyState.has_sertificate)
async def select_has_sertificate(message: Message, state: FSMContext):
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data["subject_id"])
    if message.text == "Ha":
        ignor_sertificate_names = [
            sertificate["name"] for sertificate in state_data.get("sertificates", [])
        ]
        sertificates_lst = await Sertificates.filter(subject=subject).exclude(
            name__in=ignor_sertificate_names
        )
        if not sertificates_lst:
            await state.set_state(TeachersVacancyState.position)
            await message.answer(
                "Afsuski sizning faningiz bo‘yicha boshqa sertifikat mavjud emas.",
                reply_markup=back_btn,
            )
            await message.answer(
                "Ustozlar vakansiyasi bo‘yicha lavozimni tanlang.",
                reply_markup=teacher_position_btn,
            )
            return

        await state.update_data(has_sertificate=True)
        await message.answer(
            "Sertifikatingizni tanlang.",
            reply_markup=sertifikatlar_lst_btn(
                [sert.name for sert in sertificates_lst], False
            ),
        )
        await state.set_state(TeachersVacancyState.sertificate_name)
    else:
        if state_data.get("sertificates", []) != []:
            await state.set_state(TeachersVacancyState.position)
            await message.answer("➡️", reply_markup=back_btn)
            await message.answer(
                "Ustozlar vakansiyasi bo‘yicha lavozimni tanlang.",
                reply_markup=teacher_position_btn,
            )
            return

        user = await TgUser.get_or_none(tg_id=message.chat.id)
        quiz = await Quizs.get_or_none(subject=subject)
        if not quiz:
            await state.set_state(TeachersVacancyState.position)
            await message.answer("➡️", reply_markup=back_btn)
            await message.answer(
                "Ustozlar vakansiyasi bo‘yicha lavozimni tanlang.",
                reply_markup=teacher_position_btn,
            )
            return
        answer = await QuizAnswers.get_or_none(user=user, quiz=quiz)
        if answer:
            await message.answer(
                "Siz bu testni avval topshirgansiz.", reply_markup=back_btn
            )
            if answer.correct_answers >= len(quiz.quizs) * 0.8:
                await message.answer("Siz testdan o‘tgansiz!")
                await state.set_state(TeachersVacancyState.position)
                await message.answer(
                    "Ustozlar vakansiyasi bo‘yicha lavozimni tanlang.",
                    reply_markup=teacher_position_btn,
                )
            else:
                await message.answer(
                    "Afsuski siz testdan o‘tolmadingiz!",
                    reply_markup=main_menu_users_btn(is_registered=True),
                )
                await state.clear()
            return
        await state.update_data(has_sertificate=False)
        await message.answer(
            "Siz test topshirishingiz kerak.\n\nSavollar soni:{} ta".format(
                len(quiz.quizs)
            ),
            reply_markup=ready_btn,
        )
        await state.set_state(TeachersVacancyState.ready)


@router.message(F.text, TeachersVacancyState.sertificate_name)
async def select_sertificate_name(message: Message, state: FSMContext):
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data.get("subject_id"))
    sertificate = await Sertificates.get_or_none(name=message.text, subject=subject)
    if not sertificate:
        await message.answer("Bunday sertifikat mavjud emas!")
        return
    await state.update_data(
        sertificate_id=sertificate.id,
        sertificate_name=sertificate.name,
        sertificate_ball_list=sertificate.ball_list,
    )
    await message.answer(
        "Sertifikat bo‘yicha overall ballingizni tanlang.",
        reply_markup=sertifikat_balls_lst_btn(
            [ball for ball in sertificate.ball_list], False
        ),
    )
    await state.set_state(TeachersVacancyState.sertificate_ball)


@router.message(F.text, TeachersVacancyState.sertificate_ball)
async def select_sertificate_ball(message: Message, state: FSMContext):
    await state.update_data(sertificate_ball=message.text)
    await message.answer("Endi sertifikat faylini yuboring.", reply_markup=back_btn)
    await state.set_state(TeachersVacancyState.sertificate_file)


@router.message(TeachersVacancyState.sertificate_file)
async def select_sertificate_file(message: Message, state: FSMContext):
    if not message.document and not message.photo:
        await message.answer("Iltimos, sertifikatni fayl ko‘rinishida yuboring.")
        return
    state_data = await state.get_data()
    sertificates = state_data.get("sertificates", [])
    sertificates.append(
        {
            "name": state_data["sertificate_name"],
            "ball": state_data["sertificate_ball"],
            "content_type": "document" if message.document else "photo",
            "file_id": (
                message.document.file_id
                if message.document
                else message.photo[-1].file_id
            ),
        }
    )
    await state.update_data(sertificates=sertificates)
    # TODO: vaqtincha skip - bot.get_file va download o'chirildi
    # file = await bot.get_file(
    #     message.document.file_id if message.document else message.photo[-1].file_id
    # )
    # await bot.download_file(
    #     file.file_path,
    #     destination=f"statics/sertificates/{message.document.file_id if message.document else message.photo[-1].file_id}.{file.file_path.split('.')[-1]}",
    # )
    ignor_sertificate_names = [sertificate["name"] for sertificate in sertificates]
    sertificates_lst = await Sertificates.filter(
        subject=state_data["subject_id"]
    ).exclude(name__in=ignor_sertificate_names)
    if not sertificates_lst:
        await state.set_state(TeachersVacancyState.position)
        await message.answer(
            "Ustozlar vakansiyasi bo‘yicha lavozimni tanlang.",
            reply_markup=teacher_position_btn,
        )
        return
    await state.set_state(TeachersVacancyState.has_sertificate)
    await message.answer("Yana sertifikatingiz bormi?", reply_markup=confirm_btn)


@router.message(F.text == "Tayyorman", TeachersVacancyState.ready)
async def select_ready(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(ready=message.text)
    msg = await message.answer(
        "Test boshlanmoqda...", reply_markup=ReplyKeyboardRemove()
    )
    await sleep(1)
    await state.set_state(TeachersVacancyState.quizs)
    await create_task(start_quizs(msg.message_id, state, bot, message.chat.id))


async def start_quizs(message_id: int, state: FSMContext, bot: Bot, chat_id: int):
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data["subject_id"])
    quizs = await Quizs.filter(subject=subject).first()
    await state.update_data(
        quizs_id=quizs.id,
        quizs_data=quizs.quizs,
        quiz_index=0,
        correct_answers=0,
        start_time=datetime.now(timezone.utc).isoformat(),
    )
    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    msg = await bot.send_message(chat_id, "🚀 KETDIK!", parse_mode="HTML")
    await sleep(1)
    await bot.delete_message(chat_id=chat_id, message_id=msg.message_id)

    await bot.send_poll(
        chat_id=chat_id,
        question=quizs.quizs[0]["question"],
        options=[
            *quizs.quizs[0]["options"],
        ],
        type="quiz",
        correct_option_id=quizs.quizs[0]["answer"] - 1,
        is_anonymous=False,
    )
    state_data = await state.get_data()
    start_time = datetime.fromisoformat(state_data["start_time"])
    while datetime.now(timezone.utc) - start_time < timedelta(minutes=40):
        await sleep(60)
    state_now = await state.get_state()
    state_data = await state.get_data()
    quizs_data = state_data["quizs_data"]
    if state_now == TeachersVacancyState.quizs:
        await bot.send_message(
            chat_id,
            "<tg-emoji emoji-id='5348445120700102867'>🏁</tg-emoji>",
            parse_mode="HTML",
        )
        await bot.send_message(
            chat_id,
            "<b>Testga ajratilgan vaqt tugadi!</b>\n\nTo‘g‘ri javoblar: {}\nJavoblar soni: {} ta\nSavollar soni: {} ta".format(
                state_data["correct_answers"],
                state_data["quiz_index"] + 1,
                len(quizs_data),
            ),
            parse_mode="HTML",
        )
        user = await TgUser.get_or_none(tg_id=chat_id)
        quizs = await Quizs.get_or_none(id=state_data["quizs_id"])
        await QuizAnswers.create(
            user=user,
            quiz=quizs,
            correct_answers=state_data["correct_answers"],
        )
        if state_data["correct_answers"] >= len(quizs_data) * 0.8:
            await bot.send_message(chat_id, "Siz testdan o‘tdingiz!")
            await state.set_state(TeachersVacancyState.position)
            await bot.send_message(
                chat_id,
                "Ustozlar vakansiyasi bo‘yicha lavozimni tanlang.",
                reply_markup=teacher_position_btn,
            )
        else:
            await bot.send_message(
                chat_id,
                "Afsuski siz testdan o‘tolmadingiz!",
                reply_markup=main_menu_users_btn(is_registered=True),
            )
            await state.clear()


@router.poll_answer(TeachersVacancyState.quizs)
async def poll_answer_handler(answer: PollAnswer, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    quizs_data = state_data["quizs_data"]
    quiz_index = state_data["quiz_index"]
    start_time = datetime.fromisoformat(state_data["start_time"])

    if datetime.now(timezone.utc) - start_time > timedelta(seconds=60):
        return

    if answer.option_ids[0] == int(quizs_data[quiz_index]["answer"]) - 1:
        await state.update_data(
            quiz_index=quiz_index + 1, correct_answers=state_data["correct_answers"] + 1
        )
    else:
        await state.update_data(quiz_index=quiz_index + 1)
    state_data = await state.get_data()
    if quiz_index == len(quizs_data) - 1:
        await bot.send_message(
            answer.user.id,
            "<tg-emoji emoji-id='5348445120700102867'>🏁</tg-emoji>",
            parse_mode="HTML",
        )
        await state.set_state(TeachersVacancyState.ready)
        await bot.send_message(
            answer.user.id,
            "Sizning test natijangiz:\n\nTo‘g‘ri javoblar soni: {}\nJavoblar soni: {} ta\nSavollar soni: {} ta".format(
                state_data["correct_answers"], state_data["quiz_index"], len(quizs_data)
            ),
            parse_mode="HTML",
        )
        user = await TgUser.get_or_none(tg_id=answer.user.id)
        quizs = await Quizs.get_or_none(id=state_data["quizs_id"])
        await QuizAnswers.create(
            user=user,
            quiz=quizs,
            correct_answers=state_data["correct_answers"],
        )

        if state_data["correct_answers"] >= len(quizs_data) * 0.8:
            await bot.send_message(answer.user.id, "Siz testdan o'tdingiz!")
            await state.set_state(TeachersVacancyState.position)
            await bot.send_message(
                answer.user.id,
                "Ustozlar vakansiyasi bo‘yicha lavozimni tanlang.",
                reply_markup=teacher_position_btn,
            )
        else:
            await bot.send_message(
                answer.user.id,
                "Afsuski siz testdan o‘tolmadingiz!",
                reply_markup=main_menu_users_btn(is_registered=True),
            )
            await state.clear()
    else:
        await bot.send_message(
            answer.user.id,
            "<tg-emoji emoji-id='5319018929660655484'>➡️</tg-emoji>",
            parse_mode="HTML",
        )
        await bot.send_poll(
            chat_id=answer.user.id,
            question=quizs_data[quiz_index + 1]["question"],
            options=[
                *quizs_data[quiz_index + 1]["options"],
            ],
            type="quiz",
            correct_option_id=quizs_data[quiz_index + 1]["answer"] - 1,
            is_anonymous=False,
        )


@router.callback_query(F.data.startswith("position_"))
async def select_position(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(position=callback_query.data.split("_")[1])
    await callback_query.message.edit_text(
        "Ustozlar vakansiyasi bo‘yicha lavozimni tanlang.\n\n"
        + callback_query.data.split("_")[1],
        reply_markup=None,
    )
    await state.set_state(TeachersVacancyState.are_you_student)
    state_data = await state.get_data()
    subject = await Subjects.get_or_none(id=state_data["subject_id"])
    vacansy_text = await VacanciesText.get_or_none(name=subject.name)
    if vacansy_text and vacansy_text.text.strip():
        await callback_query.message.answer(
            vacansy_text.text.strip(), parse_mode="HTML"
        )
    await callback_query.message.answer("Siz talabamisiz?", reply_markup=confirm_btn)


@router.message(F.text, TeachersVacancyState.are_you_student)
async def select_are_you_student(message: Message, state: FSMContext):
    await state.update_data(are_you_student=message.text)
    if message.text.lower() == "ha":
        await message.answer(
            "O’qiyotgan oliygohingiz, yo’nalishingiz va kursingizni kiriting?",
            reply_markup=back_btn,
        )
        await state.set_state(TeachersVacancyState.university)
    else:
        await message.answer("Bitirgan oliygohingizni kiriting?", reply_markup=back_btn)
        await state.set_state(TeachersVacancyState.university)


@router.message(F.text, TeachersVacancyState.university)
async def select_university(message: Message, state: FSMContext):
    await state.update_data(university=message.text)
    await message.answer("Sohadagi tajribangiz necha yil?", reply_markup=experience_btn)
    await state.set_state(TeachersVacancyState.experience)


@router.message(F.text, TeachersVacancyState.experience)
async def select_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    if message.text == "Hech qayerda ishlamaganman":
        await message.answer(
            "Bizdan qancha oylik maosh kutayapsiz?", reply_markup=back_btn
        )
        await state.set_state(TeachersVacancyState.salary)
        return

    await message.answer("Oxirgi ishlagan tashkilotingiz nomi?", reply_markup=back_btn)
    await state.set_state(TeachersVacancyState.last_work_place)


@router.message(F.text, TeachersVacancyState.last_work_place)
async def select_last_work_place(message: Message, state: FSMContext):
    await state.update_data(last_work_place=message.text)
    await message.answer(
        "Oxirgi ish joyingizdan ketish sababini kiriting.", reply_markup=back_btn
    )
    await state.set_state(TeachersVacancyState.why_leave_work)


@router.message(F.text, TeachersVacancyState.why_leave_work)
async def select_why_leave_work(message: Message, state: FSMContext):
    await state.update_data(why_leave_work=message.text)
    await message.answer(
        "Oxirgi ishlagan tashkilotingiz yoki to‘g‘ridan-to‘g‘ri rahbaringiz telefon raqamini qoldiring.\n\nMasalan: +998901234567",
        reply_markup=back_btn,
    )
    await state.set_state(TeachersVacancyState.last_work_place_phone)


@router.message(F.text, TeachersVacancyState.last_work_place_phone)
async def select_last_work_place_phone(message: Message, state: FSMContext):
    if not is_valid_phone(message.text):
        await message.answer(
            "Noto‘g‘ri telefon raqami! To‘g‘ri telefon raqam kiriting.\n\nMasalan, +998901234567"
        )
        return
    await state.update_data(last_work_place_phone=message.text)
    await message.answer("Bizdan qancha oylik maosh kutayapsiz?", reply_markup=back_btn)
    await state.set_state(TeachersVacancyState.salary)


@router.message(F.text, TeachersVacancyState.salary)
async def select_salary(message: Message, state: FSMContext):
    await state.update_data(salary=message.text)
    await message.answer("Nega aynan bizni tanladingiz?", reply_markup=back_btn)
    await state.set_state(TeachersVacancyState.why_choice_us)


@router.message(F.text, TeachersVacancyState.why_choice_us)
async def select_why_choice_us(message: Message, state: FSMContext):
    state_data = await state.get_data()
    user = await TgUser.get_or_none(tg_id=message.from_user.id)
    phones_text = "\n\n"
    for phone in user.phone_numbers:
        phones_text += f"\t\t• {user.phone_numbers[phone]}\n"
    else:
        phones_text += "\n"
    await message.answer(
        f"""
Siz kiritgan ma’lumotlar:

<blockquote expandable>
Ism-Familiya: {user.full_name}
Filial: {user.branch if user.branch else "Yo'q"}
Telefon raqamlar: {phones_text}
Fan: {state_data['subject_name']}
Ish vaqti: {state_data['working_time']}
Sertifikatlar:{' | '.join([ser['name'] + ' ' + ser['ball'] for ser in state_data.get('sertificates', [])])}
Oliygoh: {state_data.get('university', '')}
Tajriba: {state_data['experience']}
Lavozim: {state_data['position']}
Oxirgi ish joyi: {state_data.get("last_work_place", "Yo'q")}
Oxirgi ish joyidan ketish sababi: {state_data.get("why_leave_work", "Yo'q")}
Oxirgi ish joyi telefon raqami: {state_data.get("last_work_place_phone", "Yo'q")}
Bizdan qancha oylik maosh kutayapsiz?: {state_data['salary']}
Nega aynan bizni tanladingiz?: {message.text}
</blockquote>

Ma’lumotlaringiz to‘g‘riligini tasdiqlang.
    """,
        reply_markup=confirm_btn,
    )
    await state.update_data(why_choice_us=message.text)
    await state.set_state(TeachersVacancyState.confirm)


@router.message(TeachersVacancyState.confirm)
async def confirm(message: Message, state: FSMContext):
    if message.text.lower() == "ha":
        state_data = await state.get_data()
        user = await TgUser.get_or_none(tg_id=message.from_user.id)
        await TeacherResume.create(
            subject=state_data["subject_name"],
            working_time=state_data["working_time"],
            sertificates=state_data.get("sertificates", []),
            university=state_data.get("university", ""),
            experience=state_data["experience"],
            position=state_data["position"],
            last_work_place=state_data.get("last_work_place", "yo'q"),
            why_leave_work=state_data.get("why_leave_work", "yo'q"),
            last_work_place_phone=state_data.get("last_work_place_phone", "yo'q"),
            salary=state_data["salary"],
            why_choice_us=state_data["why_choice_us"],
            user=user,
        )
        sertificates_text = "\n\n"
        if state_data.get("sertificates"):
            sertificates_text += (
                "\n".join(
                    [
                        f"\t\t• {ser['name']} - {ser['ball']}"
                        for ser in state_data.get("sertificates", [])
                    ]
                )
                + "\n"
            )
        phones_text = "\n\n"
        for phone in user.phone_numbers:
            phones_text += f"\t\t• {user.phone_numbers[phone]}\n"
        else:
            phones_text += "\n"
        caption = f"""
Yangi rezyume qo‘shildi:

<blockquote expandable>
Ism-familiya: {user.full_name}
Filial: {user.branch}
Telefon raqamlar: {phones_text}
Fani: {state_data['subject_name']}
Ish vaqti: {state_data['working_time']}
Sertifikatlar: {sertificates_text}
Oliygoh: {state_data.get('university', '')}
Tajriba: {state_data['experience']}
Lavozim: {state_data['position']}
Oxirgi ish joyi: {state_data.get('last_work_place', "Yo'q")}
Oxirgi ish joyidan ketish sababi: {state_data.get('why_leave_work', "Yo'q")}
Oxirgi ish joyi telefon raqami: {state_data.get('last_work_place_phone', "Yo'q")}
Bizdan qancha oylik maosh kutayapsiz?: {state_data['salary']}
Nega aynan bizni tanladingiz?: {state_data['why_choice_us']}
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
                print(f"Error sending message to admin {admin}: {e}")
        last_text = await VacanciesText.get_or_none(name=state_data["subject_name"])
        if last_text and len(last_text.last_text.strip()) > 5:
            await message.answer(
                last_text.last_text,
                parse_mode="HTML",
                reply_markup=main_menu_users_btn(is_registered=True),
            )
        else:
            await message.answer(
                """
Sabr bilan shu joygacha kelganingiz uchun raxmat! Siz birinchi bosqichdan muvaffaqiyatli o'tdingiz!

Tez orada siz bilan bog‘lanamiz!
            """,
                reply_markup=main_menu_users_btn(is_registered=True),
            )
        await state.clear()
    else:
        await message.answer(
            "Ma’lumotlarni yuborish bekor qilindi!",
            reply_markup=main_menu_users_btn(is_registered=True),
        )
        await state.clear()
