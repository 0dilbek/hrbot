from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from states.user import UserRegisterState
from database.models import TgUser
from config import ADMINS
from datetime import datetime
from filters.user import IsNewUser
from keyboards.reply import skip_btn, back_btn, main_menu_users_btn, phone_btn, branches_btn
from utils import is_valid_phone, is_valid_date

router = Router()

@router.message(F.text == "Orqaga", IsNewUser())
async def register_full_name_back(message: Message, state: FSMContext):
    state_name = await state.get_state()
    match state_name:
        case UserRegisterState.phone_number1:
            await state.set_state(UserRegisterState.full_name)
            await message.answer("Ism-familiyangizni kiriting:", reply_markup=back_btn)
        case UserRegisterState.phone_number2:
            await state.set_state(UserRegisterState.phone_number1)
            await message.answer("Telefon raqamingizni yuboring:\n\n", reply_markup=skip_btn)
        case UserRegisterState.birth_date:
            await state.set_state(UserRegisterState.phone_number2)
            await message.answer("Ikkinchi telefon raqamingizni kiriting:\n\nMasalan: +998901234567", reply_markup=skip_btn)
        case UserRegisterState.born_address:
            await state.set_state(UserRegisterState.birth_date)
            await message.answer("Tug‘ilgan kuningizni kiriting:\n\nMasalan: 01.01.2000", reply_markup=back_btn)
        case UserRegisterState.live_address:
            await state.set_state(UserRegisterState.born_address)
            await message.answer("Tug‘ilgan joyingizni kiriting:", reply_markup=back_btn)
        case UserRegisterState.work_or_study_address:
            await state.set_state(UserRegisterState.live_address)
            await message.answer("Yashash joyingizni kiriting:", reply_markup=back_btn)
        case UserRegisterState.branch:
            await state.set_state(UserRegisterState.work_or_study_address)
            await message.answer("Ish yoki o‘qish joyingizni kiriting:", reply_markup=back_btn)
        case UserRegisterState.profile_pic:
            await state.set_state(UserRegisterState.branch)
            await message.answer("Qaysi filialimizga murojaat qilmoqchisiz?", reply_markup=branches_btn)
        case __:
            await message.answer("Orqaga qaytildi!!", reply_markup=main_menu_users_btn(is_registered=False))
            await state.clear()

@router.message(CommandStart(), IsNewUser())
async def start(message: Message):
    await message.answer("Assalomu alaykum, xush kelibsiz!", reply_markup=main_menu_users_btn(is_registered=False))

@router.message(F.text == "Ro‘yxatdan o‘tish", IsNewUser())
async def register(message: Message, state: FSMContext):
    await message.answer("Assalomu alaykum! Ro‘yxatdan o‘tish uchun ism-familiyangizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserRegisterState.full_name)

@router.message(UserRegisterState.full_name, F.text)
async def register_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Telefon raqamingizni yuboring", reply_markup=phone_btn)
    await state.set_state(UserRegisterState.phone_number1)

@router.message(UserRegisterState.phone_number1)
async def register_phone_number1(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Iltimos, telefon raqamingizni \"Telefon raqamimni yuborish\" tugmasi orqali yuboring:", reply_markup=phone_btn)
        return
    
    phone = message.contact.phone_number
    if phone[0] != '+':
        phone = '+' + phone
    await state.update_data(phone_number1=phone)
    await message.answer("Ikkinchi telefon raqamingizni kiriting (masalan: +998901234567):", reply_markup=back_btn)
    await state.set_state(UserRegisterState.phone_number2)

@router.message(UserRegisterState.phone_number2, F.text)
async def register_phone_number2(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not is_valid_phone(phone):
        await message.answer("Iltimos, to‘g‘ri telefon raqamini kiriting (masalan: +998901234567):")
        return
    state_data = await state.get_data()
    if state_data['phone_number1'] == phone:
        await message.answer("Iltimos, boshqa telefon raqamini kiriting:")
        return
    await state.update_data(phone_number2=phone)
    await message.answer("Tug‘ilgan kuningizni kiriting:\n\nmasalan: 17.07.2000", reply_markup=back_btn)
    await state.set_state(UserRegisterState.birth_date)

@router.message(UserRegisterState.birth_date, F.text)
async def register_birth_date(message: Message, state: FSMContext):
    date = message.text.strip()
    if not is_valid_date(date):
        await message.answer("Iltimos, to‘g‘ri sana formatini kiriting (masalan: 17.07.2000):")
        return
    await state.update_data(birth_date=date)
    await message.answer("Tug‘ilgan joyingizni kiriting:", reply_markup=back_btn)
    await state.set_state(UserRegisterState.born_address)

@router.message(UserRegisterState.born_address, F.text)
async def register_born_address(message: Message, state: FSMContext):
    await state.update_data(born_address=message.text)
    await message.answer("Yashash joyingizni kiriting:", reply_markup=back_btn)
    await state.set_state(UserRegisterState.live_address)

@router.message(UserRegisterState.live_address, F.text)
async def register_live_address(message: Message, state: FSMContext):
    await state.update_data(live_address=message.text)
    await message.answer("Ish yoki o‘qish joyingizni kiriting:", reply_markup=back_btn)
    await state.set_state(UserRegisterState.work_or_study_address)

@router.message(UserRegisterState.work_or_study_address, F.text)
async def register_work_or_study_address(message: Message, state: FSMContext):
    await state.update_data(work_or_study_address=message.text)
    await message.answer("Biz haqimizda qayerdan bildingiz?", reply_markup=back_btn)
    await state.set_state(UserRegisterState.where_find_us)

@router.message(UserRegisterState.where_find_us, F.text)
async def register_where_find_us(message: Message, state: FSMContext):
    await state.update_data(where_find_us=message.text)
    await message.answer("Qaysi filialimizga murojaat qilmoqchisiz?", reply_markup=branches_btn)
    await state.set_state(UserRegisterState.branch)

@router.message(UserRegisterState.branch, F.text)
async def register_branch(message: Message, state: FSMContext):
    await state.update_data(branch=message.text)
    await message.answer("Suratingizni yuboring:", reply_markup=skip_btn)
    await state.set_state(UserRegisterState.profile_pic)

@router.message(UserRegisterState.profile_pic)
async def register_profile_pic(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    profile_pic_file_id = ""
    profile_pic_path = ""
    if message.text:
        if message.text == "O‘tkazib yuborish":
            profile_pic_file_id = ""
            profile_pic_path = ""
        else:
            await message.answer("Iltimos, suratingizni yuboring.")
            return
    elif message.photo:
        profile_pic_file_id = message.photo[-1].file_id
        file = await bot.get_file(message.photo[-1].file_id)
        await bot.download_file(file.file_path, f"statics/photos/{message.from_user.id}.{file.file_path.split('.')[-1]}")
        profile_pic_path = f"statics/photos/{message.from_user.id}.{file.file_path.split('.')[-1]}"
    else:
        await message.answer("Iltimos, suratingizni yuboring.")
        return
    # try:
    user = await TgUser.create(
                tg_id=message.from_user.id,
                full_name=state_data['full_name'],
                phone_numbers={"phone_number1": state_data['phone_number1'], "phone_number2": state_data['phone_number2']},
                birth_date=datetime.strptime(state_data['birth_date'], "%d.%m.%Y").date(),
                born_address=state_data['born_address'],
                live_address=state_data['live_address'],
                work_or_study_address=state_data['work_or_study_address'],
                where_find_us=state_data['where_find_us'],
                branch=state_data['branch'],
                profile_pic_file_id=profile_pic_file_id,
                profile_pic_path=profile_pic_path
            )

    phones_text = "\n\n"
    for phone in user.phone_numbers:
        phones_text += f"\t\t• {user.phone_numbers[phone]}\n"
    phones_text += "\n"

    caption = f"""<b>Yangi foydalanuvchi:</b>

<blockquote expandable>
Ism-Familiya: {user.full_name}
Filial: {user.branch if user.branch else "Yo'q"}
Telefon raqamlar: {phones_text}
Tug‘ilgan sana: {user.birth_date}
Tug‘ilgan joy: {user.born_address}
Yashash joyi: {user.live_address}
Ish joyi yoki maktab: {user.work_or_study_address}
Qayerdan bizni tanladingiz: {user.where_find_us}
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

    # except Exception as e:
    #     await message.answer("Ro'yxatdan o'tishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.", reply_markup=main_menu_users_btn(is_registered=False))
    #     await state.clear()
    #     return
    await message.answer("""
Ro‘yxatdan o‘tish davom etmoqda...

Endi biz haqimizda ma'lumot olishingiz, vakansiya yo‘nalishingizni tanlashingiz yoki bizga hoziroq bog‘lanishingiz mumkin!
    """, reply_markup=main_menu_users_btn(is_registered=True))
    await state.clear()