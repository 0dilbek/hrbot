from aiogram import Router
from . import start, fanlar, admins_vacansy, reports

router = Router()
router.include_router(fanlar.router)
router.include_router(admins_vacansy.router)
router.include_router(reports.router)
router.include_router(start.router)