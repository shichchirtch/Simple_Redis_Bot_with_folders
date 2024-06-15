from aiogram import Router, F
from filters import DATA_IS_DIGIT, DATA_IS_NOT_DIGIT
from lexicon import *
from aiogram.types import Message, ReplyKeyboardRemove
from external_functions import reset, update_table, check_attempts_lost_number, get_secret_number
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from bot_states import FSM_IN_GAME
from keyboards import keyboard_after_cancel
import asyncio
game_router = Router()


@game_router.message(DATA_IS_NOT_DIGIT(), F.text.in_(positiv_answer), StateFilter(FSM_IN_GAME.after_start))
async def process_positive_answer(message: Message,  state: FSMContext):
    user_tg_id = message.from_user.id
    await get_secret_number(user_tg_id)
    await state.set_state(FSM_IN_GAME.in_game)
    # status = await state.get_state()
    # print("state.get_state = ", status)
    await message.answer(text="Я загадал число, начинайте угадывать !",
                         reply_markup=ReplyKeyboardRemove())


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@game_router.message(F.text.lower().in_(negative_answer), StateFilter(FSM_IN_GAME.after_start))
async def process_negative_answer(message: Message):
    await message.answer(text=press_cancel,
                         reply_markup=keyboard_after_cancel)


@game_router.message(StateFilter(FSM_IN_GAME.in_game), DATA_IS_DIGIT())
async def process_numbers_answer(message: Message, state: FSMContext):
    user_tg_id = message.from_user.id
    user_name = message.chat.first_name
    if await check_attempts_lost_number(user_tg_id):
            # print(f'\n Attempts for {user_name} = 0 Game done !')
            await reset(user_tg_id)  # обнуляю таблицу
            await message.answer(text=f'{user_name} {antwort}')
            await state.set_state(FSM_IN_GAME.after_start)
            await asyncio.sleep(1)
            await message.answer(text=no_att_lost)
            await message.answer(text=press_cancel, reply_markup=keyboard_after_cancel)

    else:
        res = await update_table(user_tg_id, int(message.text))
        status = await state.get_state()
        # print('\n\nstate.get_state()  =  ', type(status), status)
        if not res:
            await message.answer(text=f'<b>{user_name}</b> {antwort}',
                                 reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(text=f'<b>{user_name}</b>  + {res}',
                                 reply_markup=ReplyKeyboardRemove())


@game_router.message(StateFilter(FSM_IN_GAME.after_start, FSM_IN_GAME.in_game))
async def process_error_data(message: Message, state: FSMContext):
    user_name = message.chat.first_name
    status = await state.get_state()
    if message.text == ('/start'):
        await message.reply(restart)
    elif status == 'FSM_IN_GAME:in_game':
        await message.answer(text=f'<b>{user_name}</b>,   {in_game_wrong_data}',
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text=f'<b>{user_name}</b>,   {error}',
                             reply_markup=keyboard_after_cancel)

