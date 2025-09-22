from aiogram import Router

from bot.handlers import menu_callbacks

import sqlalchemy
from . import export_users, info, menu, start, support, settings, deepseek_message, text_inserts


def get_handlers_router() -> Router:
    router = Router()
    router.include_router(start.router)
    router.include_router(info.router)
    router.include_router(support.router)
    router.include_router(menu.router)
    router.include_router(menu_callbacks.router)
    router.include_router(export_users.router)
    router.include_router(deepseek_message.router)
    router.include_router(settings.router)
    router.include_router(text_inserts.router)
    return router
