from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.services.deepseek_client import ask_deepseek
from bot.keyboards.inline.contacts import back_button_keyboard

router = Router()


class DeepSeekStates(StatesGroup):
    waiting_for_question = State()
    processing = State()


@router.message(DeepSeekStates.waiting_for_question)
async def process_deepseek_question(message: Message, state: FSMContext):
    user_text = message.text
    await message.answer("⏳ Think...")
    await state.set_state(DeepSeekStates.processing)

    try:
        reply = ask_deepseek(user_text)
    except Exception as e:
        reply = f"Error to connect: {e}"

    await message.answer(reply, reply_markup=back_button_keyboard())
    await state.set_state(DeepSeekStates.waiting_for_question)
