from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from bot.keyboards.inline.contacts import back_button_keyboard
router = Router()


@router.callback_query(F.data == "word_count")
async def handle_word_count(callback: CallbackQuery):
    await callback.message.answer(_("You pressed word count button"), reply_markup=back_button_keyboard())
    await callback.answer()


@router.callback_query(F.data == "schedule")
async def handle_schedule(callback: CallbackQuery):
    await callback.message.answer(_("You pressed schedule button"), reply_markup=back_button_keyboard())
    await callback.answer()


@router.callback_query(F.data == "menu")
async def handle_back(callback: CallbackQuery):
    await callback.message.answer(_("Returning to menu..."), reply_markup=back_button_keyboard())
    await callback.answer()
