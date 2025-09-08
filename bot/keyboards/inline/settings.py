from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def settings_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=_("word count button"),
                              callback_data="word_count")],
        [InlineKeyboardButton(text=_("schedule button"),
                              callback_data="schedule")],
        [InlineKeyboardButton(text=_("back button"),
                              callback_data="menu")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1, 1, 1)

    return keyboard.as_markup()
