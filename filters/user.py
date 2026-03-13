from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.user import TeachersVacancyState, AdminsVacancyState
from database.models import TgUser
from config import ADMINS

class IsNewUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not await TgUser.filter(tg_id=message.from_user.id).exists()

class IsRegisteredUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await TgUser.filter(tg_id=message.from_user.id).exists()

class InTeachersResumeState(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return await state.get_state() in [
            TeachersVacancyState.subject, TeachersVacancyState.working_time, TeachersVacancyState.has_sertificate, 
            TeachersVacancyState.sertificate_name, TeachersVacancyState.sertificate_ball, TeachersVacancyState.sertificate_file, 
            TeachersVacancyState.experience, TeachersVacancyState.last_work_place, TeachersVacancyState.why_leave_work, 
            TeachersVacancyState.last_work_place_phone, TeachersVacancyState.salary, TeachersVacancyState.position, 
            TeachersVacancyState.why_choice_us, TeachersVacancyState.confirm, TeachersVacancyState.are_you_student, TeachersVacancyState.university
        ]

class InAdminsResumeState(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return await state.get_state() in [
            AdminsVacancyState.vacancy_type, AdminsVacancyState.working_time, AdminsVacancyState.foreign_language, 
            AdminsVacancyState.foreign_language_level, AdminsVacancyState.experience, AdminsVacancyState.last_work_place, 
            AdminsVacancyState.why_leave_work, AdminsVacancyState.last_work_place_phone, AdminsVacancyState.why_choice_us,
            AdminsVacancyState.confirm
        ]
