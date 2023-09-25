from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from aiogram.filters import Filter, Command
import asyncio
from environs import Env
import logging #импортируем библиотеку логирования
from aiogram.types import BotCommand, BotCommandScopeDefault #Узнать про скопы
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from pg import db_bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


#Блок инициализации#############################
# env = Env()                                    #
# env.read_env('.env')                           #
# TOKEN = env.str('TOKEN')                       #
# ADMIN = env.int('ADMIN_ID')       
TOKEN = '6326240605:AAFqzb08jfCCDcJhwUuT2Z6YfxCgFUqFh5A'
ADMIN = '6458439503'
################################################



#Блок кнопок

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='new_reservation', description='Новая бронь'),
        BotCommand(command='schedule', description='Расписание'),
        BotCommand(command='my_reservation', description='Моя история'),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault()) #Скоп по умолчанию|ПОказывает команды всем



#Машина состояний
class StepsForm(StatesGroup):
    GET_DIRECTION = State()
    GET_DATE = State()
    GET_NAME = State()
    GET_PERSONS = State()
    GET_CONTACT = State()



#Формируем кнопки через билдер from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def booking_button(state: FSMContext):
    keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
    keyboard_builder.button(text='Забронировать билет') #далее создаем кнопки

    await state.set_state(StepsForm.GET_DIRECTION)
    return keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                               one_time_leyboard=True,
                               input_field_placeholder=''                               
                               )
    


async def get_booking(message: Message, state: FSMContext):
    services = db_bot.select_services()

    keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок 
    for i in services:
        keyboard_builder.button(text=f'{i.get("service_name")}') #далее создаем кнопки

    keyboard_builder.adjust(3,3)
    await message.answer('Укажите направление',reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                               one_time_leyboard=True,
                               input_field_placeholder=''                               
                               ))
    

    await state.set_state(StepsForm.GET_DATE)



async def get_date(message: Message, state: FSMContext):
    await message.answer(f'Выберите дату поездки \n<b>{message.text}</b>', reply_markup=ReplyKeyboardRemove())


    await state.update_data(direction=message.text)  
    await state.set_state(StepsForm.GET_NAME)






################################################
#Блок стартовых функций#########################
    
async def start_bot(bot: Bot): #функция срабатывает когда запускается сервер с ботом
    await set_commands(bot)
    await bot.send_message(ADMIN, text='Бот запущен!')
async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN, text='<s>Бот остановлен</s>')

async def get_start(message: Message): #Функция срабатывает когда юзер дает команду /start
    keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
    keyboard_builder.button(text='Забронировать билет') #далее создаем кнопки
    await message.answer('Давай начнем!',reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                               one_time_leyboard=True,
                               input_field_placeholder=''
                               
                               )) #Отправляет текстовые кнопки прописанные выше



###############################################


#Тело бота#####################################
async def start():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(name)s -(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    bot = Bot(token=TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.startup.register(start_bot) #Регистрируем хэндлер срабатывающий при запуске
    dp.shutdown.register(stop_bot)



    dp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /startdp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start
    dp.message.register(get_start, Command(commands=['new_reservation'])) #Регистрируем хэндлер на команду /startdp.message.register(get_start, Command(commands=['start'])) #Регистрируем хэндлер на команду /start
    dp.message.register(get_booking, F.text=='Забронировать билет')



    dp.message.register(get_booking, StepsForm.GET_DIRECTION)         #После введении имени переходим в функцию которая
    dp.message.register(get_date, StepsForm.GET_DATE)         #После введении имени переходим в функцию которая




    try:
        #Начало сессии
        await dp.start_polling(bot)
    finally:
        #Закрываем сессию
        await bot.session.close()
###############################################


#Запускаем функцию Бота########################
if __name__ =="__main__":
    asyncio.run(start())


