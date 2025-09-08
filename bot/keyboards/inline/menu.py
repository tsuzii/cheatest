from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [InlineKeyboardButton(text=_("chatgpt button"),
                              callback_data="chatgpt")],
        [InlineKeyboardButton(text=_("text insert button"),
                              callback_data="text_insert")],
        [InlineKeyboardButton(text=_("settings button"),
                              callback_data="settings")],
        [InlineKeyboardButton(text=_("text output button"),
                              callback_data="text_output")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1, 1, 2)

    return keyboard.as_markup()
