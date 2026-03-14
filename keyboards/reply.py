from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


skip_btn = ReplyKeyboardBuilder()
skip_btn.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
skip_btn.adjust(1)
skip_btn = skip_btn.as_markup(resize_keyboard=True)

experience_btn = ReplyKeyboardBuilder()
experience_btn.button(text="Hech qayerda ishlamaganman")
experience_btn.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
experience_btn.adjust(1)
experience_btn = experience_btn.as_markup(resize_keyboard=True)

back_btn = ReplyKeyboardBuilder()
back_btn.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
back_btn = back_btn.as_markup(resize_keyboard=True)

def main_menu_users_btn(is_registered: bool):
    markup = ReplyKeyboardBuilder()
    if not is_registered:
        markup.button(text="Ro‘yxatdan o‘tish")
    else:
        markup.button(text="Vakansiyalar")
    markup.button(text="Biz haqimizda")
    markup.button(text="Bog‘lanish")
    markup.adjust(1, 2)
    return markup.as_markup(resize_keyboard=True)

vacancies_btn = ReplyKeyboardBuilder()
vacancies_btn.button(text="Ustozlarga")
vacancies_btn.button(text="Adminlarga")
vacancies_btn.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
vacancies_btn.adjust(2)
vacancies_btn = vacancies_btn.as_markup(resize_keyboard=True)

admin_menu = ReplyKeyboardBuilder()
admin_menu.button(text="Fanlar")
admin_menu.button(text="Kasblar")
admin_menu.button(text="Hisobotlar")
admin_menu.adjust(2)
admin_menu = admin_menu.as_markup(resize_keyboard=True)

def kasblar_lst_btn(kasblar: list[str], is_admin: bool):
    markup = ReplyKeyboardBuilder()
    markup.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
    sizes = [1]
    
    for kasb in kasblar:
        markup.button(text=kasb)

    count = len(kasblar)
    if count <= 5:
        width = 4
    elif count <= 10:
        width = 3
    elif count <= 15:
        width = 2
    else:
        width = 1

    if count > 0:
        full_rows = count // width
        remainder = count % width
        sizes.extend([width] * full_rows)
        if remainder > 0:
            sizes.append(remainder)

    if is_admin:
        markup.button(text="Yangi kasb qo‘shish")
        sizes.append(1)

    markup.adjust(*sizes)
    return markup.as_markup(resize_keyboard=True)

def admin_kasb_detail_btn():
    markup = ReplyKeyboardBuilder()
    markup.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
    markup.button(text="Vakansiya matnini yangilash")
    markup.button(text="Oxirgi matnni yangilash")
    markup.button(text="Kasbni o‘chirish")
    markup.adjust(1)
    return markup.as_markup(resize_keyboard=True)

def fanlar_lst_btn(fanlar: list[str], is_admin: bool):
    markup = ReplyKeyboardBuilder()
    markup.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
    sizes = [1]
    
    for fan in fanlar:
        markup.button(text=fan)

    count = len(fanlar)
    if count <= 5:
        width = 4
    elif count <= 10:
        width = 3
    elif count <= 15:
        width = 2
    else:
        width = 1

    if count > 0:
        full_rows = count // width
        remainder = count % width
        sizes.extend([width] * full_rows)
        if remainder > 0:
            sizes.append(remainder)

    if is_admin:
        markup.button(text="Yangi fan qo‘shish")
        sizes.append(1)
    


    markup.adjust(*sizes)
    return markup.as_markup(resize_keyboard=True)

def sertifikatlar_lst_btn(sertifikatlar: list[str], is_admin: bool):
    markup = ReplyKeyboardBuilder()
    markup.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
    sizes = [1]
    
    for sertifikat in sertifikatlar:
        markup.button(text=sertifikat)

    count = len(sertifikatlar)
    if count <= 5:
        width = 4
    elif count <= 10:
        width = 3
    elif count <= 15:
        width = 2
    else:
        width = 1

    if count > 0:
        full_rows = count // width
        remainder = count % width
        sizes.extend([width] * full_rows)
        if remainder > 0:
            sizes.append(remainder)

    if is_admin:
        markup.button(text="Yangi sertifikat qo‘shish")
        markup.button(text="Vakansiya matnini yangilash")
        markup.button(text="Oxirgi matnni yangilash")
        markup.button(text="Test faylini yangilash")
        markup.button(text="Shablon faylni olish")
        markup.button(text="Fanni o‘chirish")
        sizes.append(1)
    
    markup.adjust(*sizes)
    return markup.as_markup(resize_keyboard=True)

def sertifikat_balls_lst_btn(balls: list[str], is_admin: bool, is_new : bool = False):
    markup = ReplyKeyboardBuilder()
    markup.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
    sizes = [1]
    
    for ball in balls:
        markup.button(text=ball)

    count = len(balls)
    if count <= 5:
        width = 4
    elif count <= 10:
        width = 3
    elif count <= 15:
        width = 2
    else:
        width = 1

    if count > 0:
        full_rows = count // width
        remainder = count % width
        sizes.extend([width] * full_rows)
        if remainder > 0:
            sizes.append(remainder)

    if is_admin and count and is_new:
        markup.button(text="Tugadi")
        sizes.append(1)
    elif is_admin and not is_new:
        markup.button(text="Ball qo‘shish")
        markup.button(text="Ball o‘chirish")
        markup.button(text="Sertifikatni o‘chirish")
        sizes.append(2)
    
    markup.adjust(*sizes)
    return markup.as_markup(resize_keyboard=True)

working_time_btn = ReplyKeyboardBuilder()
working_time_btn.button(text="09:00 - 20:00")
working_time_btn.button(text="08:00 - 17:00")
working_time_btn.button(text="14:00 - 20:00")
working_time_btn.button(text="08:00 - 20:00")
working_time_btn.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
working_time_btn.adjust(2)
working_time_btn = working_time_btn.as_markup(resize_keyboard=True)

confirm_btn = ReplyKeyboardBuilder()
confirm_btn.button(text="Ha")
confirm_btn.button(text="Yo‘q")
confirm_btn.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
confirm_btn.adjust(2)
confirm_btn = confirm_btn.as_markup(resize_keyboard=True)

ready_btn = ReplyKeyboardBuilder()
ready_btn.button(text="Tayyorman", style="success")
ready_btn.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
ready_btn.adjust(1)
ready_btn = ready_btn.as_markup(resize_keyboard=True)

reports_menu = ReplyKeyboardBuilder()
reports_menu.button(text="Excel hisobot")
reports_menu.button(text="Sertifikatni ko‘rish")
reports_menu.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
reports_menu.adjust(1)
reports_menu = reports_menu.as_markup(resize_keyboard=True)

phone_btn = ReplyKeyboardBuilder()
phone_btn.button(text="Telefon raqamimni yuborish", request_contact=True, style="primary")
phone_btn.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
phone_btn.adjust(1)
phone_btn = phone_btn.as_markup(resize_keyboard=True)

branches_btn = ReplyKeyboardBuilder()
branches_btn.button(text="Algoritm")
branches_btn.button(text="Yangihayot")
branches_btn.button(text="Kesh")
branches_btn.button(text="Orqaga", icon_custom_emoji_id="5400169738263352182")
branches_btn.adjust(1)
branches_btn = branches_btn.as_markup(resize_keyboard=True)
