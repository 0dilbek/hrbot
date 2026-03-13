from aiogram.fsm.state import State, StatesGroup

class AdminSubjectStates(StatesGroup):

    add_fan = State()
    select_fan = State()

    add_sertifikat = State()
    add_sertifikat_balls = State()
    select_sertifikat = State()
    add_ball = State()
    delete_ball = State()
    view_balls = State()

    update_quiz = State()
    update_vacancy_text = State()
    update_last_text = State()

class AdminKasbStates(StatesGroup):
    select_kasb = State()
    about_kasb = State()
    add_kasb = State()
    add_kasb_text = State()

    update_vacancy_text = State()
    update_last_text = State()

class GetSertificateFIleState(StatesGroup):
    tg_id = State()