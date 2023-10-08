import time
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Filter, Command
import asyncio
from environs import Env
import logging #импортируем библиотеку логирования
from aiogram.types import BotCommand, BotCommandScopeDefault #Узнать про скопы
from aiogram.types import Message, ContentType, Contact
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.utils.keyboard import  ReplyKeyboardBuilder, InlineKeyboardButton
from pg import db_bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from function import number_validator, get_days, check_date_format, format_date, week_days_names
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

#Блок инициализации#############################
# env = Env()                                    #
# env.read_env('.env')                           #
# TOKEN = env.str('TOKEN')                       #
# ADMIN = env.int('ADMIN_ID')       
TOKEN = '6350482555:AAHcWVe18JERE1xOC0_jv3MvqzOXFhRI5HY'
ADMIN = '6458439503'
ADMINS = ['5767451685','6458439503']
################################################



#Блок кнопок

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='post', description='Новая бронь'),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault()) #Скоп по умолчанию|ПОказывает команды всем

async def post_post(message: Message):
    # await bot.send_message(ADMIN, 'Hello')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[ [
                InlineKeyboardButton(text='Заказать билеты', url='https://t.me/OsessaBussTour_bot'),
            ]
        ])
    if str(message.from_user.id) in ADMINS:
        await message.answer(text='Теперь доступна онлайн бронь билетов через телеграм бот', reply_markup=keyboard)


###############################################


#Тело бота#####################################
async def start():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()


    dp.message.register(post_post, F.text=='Запостить пост')

    try:
        
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию
        await bot.session.close()
###############################################


#Запускаем функцию Бота########################
if __name__ =="__main__":
    asyncio.run(start())


