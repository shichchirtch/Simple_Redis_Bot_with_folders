from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from lexicon import start_greeding, press_cancel, pre_start, game_rules
from aiogram.types import Message
from external_functions import (insert_new_user_in_table, reset,
                                check_user_in_table, time_counter, get_start_time_from_table)
from aiogram.fsm.context import FSMContext
from keyboards import  keyboard_after_cancel
from bot_states import FSM_IN_GAME
from filters import START_ONCE_ONLY

command_router = Router()

@command_router.message(START_ONCE_ONLY(), ~CommandStart())
async def before_start(message:Message):
    await message.reply(text='Нажми на кнопку <b>start</b> !',
                         reply_markup=keyboard_after_cancel)

@command_router.message(CommandStart(), START_ONCE_ONLY())
async def start_command(message: Message, state: FSMContext):
    # print(f'user {message.chat.first_name} press start')
    status = await state.get_state()
    # print('\n1 state.get_state()  =  ', type(status), status)
    user_name = message.chat.first_name
    user_tg_id = message.from_user.id
    await insert_new_user_in_table(user_tg_id, user_name)

    await state.set_state(FSM_IN_GAME.after_start)
    status = await state.get_state()
    # print('\nstate.get_state()  =  ', type(status), status)
    await message.answer(
        f'Привет, <b>{message.chat.first_name}</b> !  \U0001F60A\n {start_greeding}',
                    reply_markup=keyboard_after_cancel)
    print("Process finfshed")

@command_router.message(Command(commands='help'))
async def process_help_command(message: Message):
    # print("HELP START WORKS")
    user_tg_id = message.from_user.id
    if await check_user_in_table(user_tg_id):
        # print('we are here into help')

        await message.answer(text=game_rules)
    else:
        await message.answer('Для начала работы с ботом введите /start')
    print("HELP FINISHED !!!")


@command_router.message(Command(commands='cancel'), StateFilter(FSM_IN_GAME.in_game, FSM_IN_GAME.after_start))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text=f'Вы вышли из игры\n\n{press_cancel}', reply_markup=keyboard_after_cancel)
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    user_tg_id = message.from_user.id
    await reset(user_tg_id)
    await state.set_state(FSM_IN_GAME.after_start)



@command_router.message(F.text.in_(['/schet','Узнать Счёт', 'VS']))
async def uznatb_schet(message: Message):
    # print('\n\nузнать счет работает  ! ')
    us_tg_id = message.from_user.id
    if not await check_user_in_table(us_tg_id):
        await message.reply(pre_start)
    else:
        user_start_time = await get_start_time_from_table(us_tg_id)
        time_data = await time_counter(user_start_time)
        await message.answer(f"<b><i>{us_tg_id} : in game</i></b>\n"
                                 f'{time_data}')
