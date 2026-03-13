from aiogram import Router
from handlers.user import router as user_router
from handlers.admin import router as admin_router

router = Router()
router.include_router(admin_router)
router.include_router(user_router)