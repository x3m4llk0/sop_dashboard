from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from tgbot.db.schemas.user import Quarter

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, delete


echo_router = Router()


@echo_router.message(F.text)
async def bot_echo(message: types.Message, session: Session):
    text = await get_items(session)

    await message.answer(text)


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f'Ехо у стані {hcode(state_name)}',
        'Зміст повідомлення:',
        hcode(message.text)
    ]
    await message.answer('\n'.join(text))






async def get_items(session: Session) -> list[Quarter]:
    """Select all items"""

    q = select(Quarter)

    res = await session.execute(q)

    return res.scalars().all()