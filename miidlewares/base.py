from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from config import ADMINS
from typing import Callable, Dict, Any, Awaitable

class LongMessageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event.message, Message) and event.message.from_user.id not in ADMINS and event.message.text and len(event.message.text) > 255:
            await event.message.answer("Xabar 255 ta belgidan oshmasligi kerak.")
            return
        return await handler(event, data)