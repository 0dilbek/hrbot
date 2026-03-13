from aiogram import types
from aiogram.filters import BaseFilter
from states.admin import AdminSubjectStates, AdminKasbStates
from aiogram.fsm.context import FSMContext
from config import ADMINS

class InFanlarStateGroup(BaseFilter):
    async def __call__(self, message: types.Message, state: FSMContext) -> bool:
        state_now = await state.get_state()
        return state_now in [AdminSubjectStates.select_fan, AdminSubjectStates.add_fan, AdminSubjectStates.add_sertifikat, AdminSubjectStates.add_sertifikat_balls, AdminSubjectStates.select_sertifikat, AdminSubjectStates.view_balls, AdminSubjectStates.add_ball, AdminSubjectStates.delete_ball, AdminSubjectStates.update_quiz, AdminSubjectStates.update_vacancy_text]

class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.from_user.id in ADMINS

class InKasblarStateGroup(BaseFilter):
    async def __call__(self, message: types.Message, state: FSMContext) -> bool:
        state_now = await state.get_state()
        return state_now in [AdminKasbStates.select_kasb, AdminKasbStates.add_kasb, AdminKasbStates.add_kasb_text, AdminKasbStates.about_kasb, AdminKasbStates.update_vacancy_text]
