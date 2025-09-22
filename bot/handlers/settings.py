from bot.services.users import get_word_count, set_word_count, get_schedule, set_schedule
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.utils.i18n import gettext as _
from bot.keyboards.inline.contacts import back_button_keyboard
from sqlalchemy.ext.asyncio import AsyncSession
router = Router()


def word_count_keyboard():
    kb = InlineKeyboardBuilder()
    for val in [2, 4, 6, 8]:
        kb.button(text=str(val), callback_data=f"set_word_count:{val}")
    kb.button(text="⬅️ Назад", callback_data="menu")
    return kb.as_markup()


@router.callback_query(F.data == "word_count")
async def handle_word_count(callback: CallbackQuery, session: AsyncSession):
    current = await get_word_count(session, callback.from_user.id)
    await callback.message.answer(
        _(f"Текущее значение слов в сообщении = {current}\n\nВыберите новое:"),
        reply_markup=word_count_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("set_word_count"))
async def set_word_count_handler(callback: CallbackQuery, session: AsyncSession):
    value = int(callback.data.split(":")[1])
    await set_word_count(session, callback.from_user.id, value)
    await callback.message.answer(_(f"✅ Установлено количество слов: {value}"), reply_markup=back_button_keyboard())
    await callback.answer()


@router.callback_query(F.data == "schedule")
async def handle_schedule(callback: CallbackQuery, session: AsyncSession):
    current = await get_schedule(session, callback.from_user.id)
    await callback.message.answer(
        _(f"Текущее расписание = {current} минут\n\nВведите новое значение (в минутах):"),
        reply_markup=back_button_keyboard()
    )
    await callback.answer()


@router.message(F.text.regexp(r"^\d+$"))
async def set_schedule_handler(message: Message, session: AsyncSession):
    minutes = int(message.text)
    await set_schedule(session, message.from_user.id, minutes)
    await message.answer(_(f"✅ Расписание обновлено: {minutes} минут"), reply_markup=back_button_keyboard())


@router.callback_query(F.data == "menu")
async def handle_back(callback: CallbackQuery):
    await callback.message.answer(_("Returning to menu..."), reply_markup=back_button_keyboard())
    await callback.answer()
