from aiogram import Router
from . import start, register, teachers_vacancy, admins_vanacies

router = Router()
router.include_router(register.router)
router.include_router(admins_vanacies.router)
router.include_router(teachers_vacancy.router)
router.include_router(start.router)