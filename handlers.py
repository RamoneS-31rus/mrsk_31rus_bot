from datetime import datetime
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F 
from aiogram import Router

from extensions import (
    get_data_planned, get_data_emergency, get_data_unplanned, 
    get_data_search_planned, get_data_search_emergency, get_data_search_unplanned
    )
from keyboards import keyboard_main


router = Router()

MAX_MESS_LENGTH = 4095
date_now = datetime.now().strftime("%Y-%m-%d %H:%M")

@router.message(Command('start'))
async def cmd_start(message: Message):    
    await message.answer("Введите название улицы или нажмите соответствующею запросу кнопку", reply_markup=keyboard_main)


@router.message(Command('информация'))
async def get_info(message: Message):    
    await message.answer("тест", reply_markup=keyboard_main)


@router.message(Command('плановые'))
async def get_planned(message: Message):
    data = get_data_planned()    
    if data:        
        data = "<b>Плановые отключения:</b>\n" + data        
        if len(data) > MAX_MESS_LENGTH:            
            for x in range(0, len(data), MAX_MESS_LENGTH):                
                await message.answer(data[x:x + MAX_MESS_LENGTH])
        else:            
            await message.answer(data)
    else:
        await message.answer(f"<b>Плановых отключений нет</b>")
    with open('logs/requests.log', mode='a', encoding='utf8') as file:
        file.write(''.join(f'{date_now} - id:{message.from_user.id} - t.me/{message.from_user.username} - Плановые отключения\n'))

@router.message(Command('аварийные'))
async def get_emergency(message: Message):
    data = get_data_emergency()
    if data:
        data = "<b>Аварийные отключения:</b>\n" + data        
        if len(data) > MAX_MESS_LENGTH:
            for x in range(0, len(data), MAX_MESS_LENGTH):
                await message.answer(data[x: x + MAX_MESS_LENGTH])
        else:
            await message.answer(data)
    else:
        await message.answer(f"<b>Аварийных отключений нет</b>")
    with open('logs/requests.log', mode='a', encoding='utf8') as file:
        file.write(''.join(f'{date_now} - id:{message.from_user.id} - t.me/{message.from_user.username} - Аварийные отключения\n'))


@router.message(Command('внерегламентные'))
async def get_unplanned(message: Message):
    data = get_data_unplanned()
    if data:
        data = "<b>Внерегламентные отключения:</b>\n" + data               
        if len(data) > MAX_MESS_LENGTH:            
            for x in range(0, len(data), MAX_MESS_LENGTH):
               await message.answer(data[x:x + MAX_MESS_LENGTH])
        else:           
           await message.answer(data)
    else:
       await message.answer(f"<b>Внерегламентных отключений нет</b>")
    with open('logs/requests.log', mode='a', encoding='utf8') as file:
        file.write(''.join(f'{date_now} - id:{message.from_user.id} - t.me/{message.from_user.username} - Внерегламентные отключения\n'))


@router.message(F.text)
async def search_street(message: Message):
    data_planned = get_data_search_planned(message.text.capitalize())
    data_emergency = get_data_search_emergency(message.text.capitalize())    
    data_unplanned = get_data_search_unplanned(message.text.capitalize())      
        
    if data_planned:
        text_planned = f"<b>Плановые отключения:</b>\n{data_planned}\n"
    else:
        text_planned = ""
    if data_emergency:
        text_emergency = f"<b>Аварийные отключения:</b>\n{data_emergency}\n"
    else:
        text_emergency = ""
    if data_unplanned:
        text_unplanned = f"<b>Внерегламентные отключения:</b>\n{data_unplanned}\n"
    else:
        text_unplanned = ""    
    
    if not data_planned and not data_emergency and not data_unplanned:
        await message.answer(f"<b>Отключений нет!</b>", reply_markup=keyboard_main)
    else:
        await message.answer(f"{text_planned}{text_emergency}{text_unplanned}", reply_markup=keyboard_main)
    with open('logs/requests.log', mode='a', encoding='utf8') as file:
        file.write(''.join(f'{date_now} - id:{message.from_user.id} - t.me/{message.from_user.username} - Поиск: {message.text}\n'))