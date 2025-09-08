from aiogram import Router, types
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.core.config import settings
from bot.keyboards.inline.settings import settings_keyboard
from bot.keyboards.inline.menu import main_keyboard
from bot.keyboards.inline.contacts import back_button_keyboard

router = Router(name="menu_callbacks")


@router.callback_query(lambda c: c.data == "chatgpt")
async def chatgpt_callback(callback: CallbackQuery):
    await callback.message.answer(_("Enter your question"), reply_markup=back_button_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data == "text_insert")
async def text_insert_callback(callback: CallbackQuery):
    await callback.message.answer(_("You pressed Text Insert!"))


@router.callback_query(lambda c: c.data == "settings")
async def settings_callback(callback: CallbackQuery):
    await callback.message.answer(_("settings keyboard"), reply_markup=settings_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data == "text_output")
async def text_output_callback(callback: CallbackQuery):
    await callback.message.answer(_("You pressed Text Output!"))


@router.callback_query(lambda c: c.data == "menu")
async def settings_callback(callback: CallbackQuery):
    await callback.message.answer(_("title main keyboard"), reply_markup=main_keyboard())
    await callback.answer()
