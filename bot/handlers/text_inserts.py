from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.models.text_insert import TextInsertModel

router = Router()


class InsertTextState(StatesGroup):
    waiting_for_text = State()


@router.message(InsertTextState.waiting_for_text)
async def save_text_insert(message: Message, state: FSMContext, session: AsyncSession):
    user_id = message.from_user.id

    new_insert = TextInsertModel(user_id=user_id, text=message.text)
    session.add(new_insert)
    await session.commit()
    await session.refresh(new_insert)

    await message.answer(f"✅ Text saved (ID: {new_insert.id})")
    await state.clear()
