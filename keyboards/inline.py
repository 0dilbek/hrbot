from aiogram.utils.keyboard import InlineKeyboardBuilder

def inline_keyboard_builder(buttons: list[tuple[str, str]]):
    builder = InlineKeyboardBuilder()
    for text, callback_data in buttons:
        builder.button(text=text, callback_data=callback_data)
    return builder.as_markup()

teacher_position_btn = inline_keyboard_builder(
    [
        ("Asosiy ustoz", "position_asosiy"),
        ("Yordamchi ustoz", "position_yordamchi"),
    ]
)

def branches_btn(selected_branch: str = None):
    branches_btn = InlineKeyboardBuilder()
    branches_btn.button(text="Algoritm filiali", callback_data="branch_algoritm", style=("success" if selected_branch == "algoritm" else "primary"))
    branches_btn.button(text="Yangihayot filiali", callback_data="branch_yangihayot", style=("success" if selected_branch == "yangihayot" else "primary"))
    branches_btn.button(text="Kesh filiali", callback_data="branch_kesh", style=("success" if selected_branch == "kesh" else "primary"))
    branches_btn.adjust(1)

    return branches_btn.as_markup()
