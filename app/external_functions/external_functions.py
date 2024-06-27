from bot_base import session_marker, User
from random import randint
from sqlalchemy import select
import time

async def insert_new_user_in_table(user_tg_id:int, name:str):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.id == user_tg_id))
        print('query =', query)
        needed_data = query.scalar()
        print('needed_data = ', needed_data)
        start_time = int(time.monotonic())
        if not needed_data:
            print("********************************************")
            new_us = User(id=user_tg_id, user_name=name, start_time=start_time)
            session.add(new_us)
            print('???????????????????????????????????????????????')
            await session.commit()

async def get_secret_number(user_tg_id:int):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.id == user_tg_id))
        needed_data = query.scalar()
        needed_data.secret_number = randint(1, 100)
        await session.commit()

async def return_secret_number(user_tg_id:int):
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.id == user_tg_id))
        needed_data = query.scalar()
        secret_number = needed_data.secret_number
        return secret_number


async def update_table(user_tg_id:int, us_number:int):
    """Функция обновляет таблицу users"""
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.id == user_tg_id))
        n = query.scalar()
        data_in = n.steps
        if us_number not in n.steps:
            n.attempts -= 1  # декремент попыток
            print('\n\nn.steps =  ', n.steps)
            n.steps = data_in + [[us_number]]
            print('n.steps =  ', n.steps, '\n\n')
            await session.commit()
            return None
        else:
            await session.commit()
            return "Do not repeat your numbers !"


async def check_attempts_lost_number(user_tg_id:int):
    '''Функция проверяет количество оставшихся попыток'''
    async with session_marker() as session:
        query = await session.execute(select(User).filter(User.id == user_tg_id))
        needed_data = query.scalar()
        print('\n\n\nneeded_data.attempts', needed_data.attempts)
        if needed_data.attempts == 1:
            return True
        return False

async def reset(user_tg_id:int):
    async with session_marker() as session:
        print("\n\nWork RESET Function")
        query = await session.execute(select(User).filter(User.id == user_tg_id))
        n = query.scalar()
        n.attempts = 5
        n.steps = []
        n.secret_number = 0
        await session.commit()


async def check_user_in_table(user_tg_id:int):
    """Функция проверяет есть ли юзер в БД"""
    async with session_marker() as session:
        print("\nWork check_user Function")
        query = await session.execute(select(User).filter(User.id == user_tg_id))
        return query.one_or_none()

async def get_start_time_from_table(user_tg_id:int)->int:
    async with session_marker() as session:
        print("\n\nWork get_start_time Function")
        query = await session.execute(select(User).filter(User.id == user_tg_id))
        n = query.scalar()
        return n.start_time

async def time_counter(start_time)-> str:
    """Функция возвращает время в игре"""
    current_time = int(time.monotonic())
    if current_time - start_time < 3600:
        secund = (current_time - start_time) % 60
        minut = (current_time - start_time) // 60
        time_data = f'<b><i>GameTiming : {int(minut)} min, {int(secund)} sec.</i></b>'
        return time_data
    if 3600 < current_time - start_time < 3600*24:
        time_data = '<b><i>More then 1 hour</i></b>'
        return time_data
    else:
        time_data = '<b><i>More then 1 day</i></b>'
        return time_data













