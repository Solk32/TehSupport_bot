from typing import Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker



class DBMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker: async_sessionmaker):
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler,
        event: TelegramObject,
        data: Dict[str, Any]
    ):
        async with self.sessionmaker() as session:
            data['session'] = session
            return await handler(event, data)
