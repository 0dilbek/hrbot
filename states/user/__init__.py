from aiogram.fsm.state import State, StatesGroup

class UserRegisterState(StatesGroup):
    full_name = State()
    phone_number1 = State()
    phone_number2 = State()
    birth_date = State()
    born_address = State()
    live_address = State()
    work_or_study_address = State()
    source_of_income = State()
    where_find_us = State()
    branch = State()
    profile_pic = State()

class VacanciesState(StatesGroup):
    vacancy_type = State()

class TeachersVacancyState(StatesGroup):
    subject = State()
    working_time = State()
    has_sertificate = State()
    sertificate_name = State()
    sertificate_ball = State()
    sertificate_file = State()
    position = State()
    are_you_student = State()
    university = State()
    experience = State()
    last_work_place = State()
    why_leave_work = State()
    last_work_place_phone = State()
    salary = State()
    why_choice_us = State()
    confirm = State()


    ready = State()
    quizs = State()

class AdminsVacancyState(StatesGroup):
    vacancy_type = State()
    working_time = State()
    foreign_language = State()
    foreign_language_level = State()
    continue_foreign_language = State()
    experience = State()
    last_work_place = State()
    why_leave_work = State()
    last_work_place_phone = State()
    why_choice_us = State()
    confirm = State()