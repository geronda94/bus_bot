from aiogram import Bot, Dispatcher, F
from aiogram.filters import Filter, Command
import asyncio
from environs import Env
import logging #импортируем библиотеку логирования
from aiogram.types import BotCommand, BotCommandScopeDefault #Узнать про скопы
from aiogram.types import Message, ContentType, Contact
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,KeyboardButtonPollType, ReplyKeyboardRemove
from aiogram.utils.keyboard import  ReplyKeyboardBuilder

from pg import db_bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from function import number_validator, get_days, check_date_format, format_date, week_days_names



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


#Формруем кнопки календаря



#Машина состояний
class StepsForm(StatesGroup):
    GET_DIRECTION = State()
    GET_DATE = State()
    GET_CONTACT = State()
    GET_PERSONS = State()
    CONFIRM_BOOKING = State()


#Формируем кнопки через билдер from aiogram.utils.keyboard import ReplyKeyboardBuilder
async def booking_button(state: FSMContext):
    await state.clear()
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

    keyboard_builder.adjust(1,)
    await message.answer('Укажите направление',reply_markup=keyboard_builder.as_markup(
                                #resize_keyboard=True, #Указываем настройки клавиатуры
                               one_time_leyboard=True,
                               input_field_placeholder=''                               
                               ))
    

    await state.set_state(StepsForm.GET_DATE)


async def get_date(message: Message, state: FSMContext):
    services = db_bot.select_services()
    services_list = [x.get('service_name') for x in services]
    context_data = await state.get_data()
    state_direction = context_data.get('direction')


    if message.text in services_list:
        
        calendar_list = []
        service_days = ''

        for service in services:
            if str(message.text) == (service.get('service_name')):
                service_days = service.get('week_days')
                service_price = service.get('service_price')


        days_list = get_days(service_days).items()
        print(days_list)
        for month_name, date_list in days_list:
            calendar_list.append([KeyboardButton(text=f'{month_name}')])            
    
            date_list_buttons = []
            count_days = 0
            last_count = len(date_list) %5

            for i in range(len(date_list)):
                day = date_list[i]

                date_list_buttons.append(KeyboardButton(text=f'{day}'))
                count_days +=1           
                

                
                if count_days == 5:
                    calendar_list.append(date_list_buttons)
                    count_days = 0
                    date_list_buttons = []
                if (len(date_list) - i < 5) and (last_count == count_days):
                        for i in range(5- len(date_list_buttons)):
                            date_list_buttons.append(KeyboardButton(text=f'  '))
                        calendar_list.append(date_list_buttons)
                        count_days = 0
                        date_list_buttons = []

                            

    
        #await message.answer(f'Рейс: <b>{message.text}</b>', reply_markup=ReplyKeyboardRemove())
        await message.answer(f'Рейс: <b>{message.text}</b> \nОтправление: <b>{week_days_names(service_days=service_days)}</b>\nЦена билета: <b>{service_price} грн. </b>')
        


        await message.answer("Выберите дату отправления", reply_markup=ReplyKeyboardMarkup(keyboard=calendar_list,
                                                                        resize_keyboard=True, #Делает кнопки меньше
                                                                        one_time_keyboard=True, #Скрывает клавиатуру после нажатия
                                                                        input_field_placeholder='Нельзя вводить текст, выберите кнопку', #Подсказка в виде надписи в поле ввода
                                                                        selective=True #Показывает клавиатуру только тому кто ее вызвал(актуально в группах)
                                                                        ))

        await state.update_data(direction=message.text)  
        await state.set_state(StepsForm.GET_CONTACT)
    
    elif state_direction:
        await message.answer(f'Рейс: <b>{state_direction}</b>', reply_markup=ReplyKeyboardMarkup(keyboard=calendar_list,
                                                                        resize_keyboard=True, #Делает кнопки меньше
                                                                        one_time_keyboard=True, #Скрывает клавиатуру после нажатия
                                                                        input_field_placeholder='Нельзя вводить текст, выберите кнопку', #Подсказка в виде надписи в поле ввода
                                                                        selective=True #Показывает клавиатуру только тому кто ее вызвал(актуально в группах)
                                                                        ))

        await state.set_state(StepsForm.GET_CONTACT)
    else:
        keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
        keyboard_builder.button(text='Вернуться к выбору направления') #далее создаем кнопки


        await message.answer(f'Неверное направление, повторите ввод', 
                                reply_markup=keyboard_builder.as_markup( #Указываем настройки клавиатуры
                                                                        one_time_leyboard=True,
                                                                        input_field_placeholder=''))
        await state.set_state(StepsForm.GET_DIRECTION)


async def get_contact(message: Message, bot: Bot, state: FSMContext):
    context_data = await state.get_data()
    state_date = context_data.get('date')

    if check_date_format(message.text):
        keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
        keyboard_builder.button(text='Отправить текущий номер из Telegram', request_contact=True)
        await message.answer('Ваши данные для связи: ', reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                                one_time_leyboard=True,
                                input_field_placeholder=''                               
                                ))
        
        await state.update_data(date=message.text)
        await state.set_state(StepsForm.GET_PERSONS)
    
    elif state_date:
        keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
        keyboard_builder.button(text='Отправить текущий номер из Telegram', request_contact=True)
        await message.answer('Ваши данные для связи: ', reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                                one_time_leyboard=True,
                                input_field_placeholder=''                               
                                ))
        await state.set_state(StepsForm.GET_PERSONS)


    else:
        keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
        keyboard_builder.button(text='Вернуться к вводу даты') #далее создаем кнопки


        await message.answer(f'Неверный формат даты, повторите ввод', 
                                reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                                one_time_leyboard=True,
                                input_field_placeholder=''                               
                                )
                            )
        await state.set_state(StepsForm.GET_DATE)



async def get_persons(message: Message, state:FSMContext):

    context_data = await state.get_data()
    state_contact = context_data.get('contact')

    keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
    for i in range(1,9):
        keyboard_builder.button(text=f'{i}') #далее создаем кнопки


    if not state_contact:
        if message.contact:
            phone = message.contact.phone_number
            await message.answer('Количество пассажиров: ', reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                                    one_time_leyboard=True,
                                    input_field_placeholder='' ))
            await state.update_data(contact=message.contact.phone_number)
            await state.set_state(StepsForm.CONFIRM_BOOKING)
        else:
            phone = number_validator(message.text)
            if number_validator(phone):
                await message.answer('Количество пассажиров: ', reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                                    one_time_leyboard=True,
                                    input_field_placeholder=''))
                
                await state.update_data(contact=phone)
                await state.set_state(StepsForm.CONFIRM_BOOKING)
            else:
                keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
                keyboard_builder.button(text='Вернуться к вводу телефона') #далее создаем кнопки


                await message.answer(f'Неверный номер {message.text}, повторите ввод', 
                                        reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                                        one_time_leyboard=True,
                                        input_field_placeholder=''                               
                                        )
                                    )
                await state.set_state(StepsForm.GET_CONTACT)
    else:
        await message.answer('Количество пассажиров: ', reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                    one_time_leyboard=True,
                    input_field_placeholder=''))

        await state.set_state(StepsForm.CONFIRM_BOOKING)

    
    

async def confirm_booking(message: Message, state: FSMContext, bot: Bot):
    if message.text.isdigit():
        await state.update_data(persons=message.text)
        context_data = await state.get_data()

        direction = context_data.get('direction')
        date = format_date(context_data.get('date')).strftime('%Y-%m-%d')
        contact = context_data.get('contact')
        persons = context_data.get('persons')



        ticket_price = 0
        total_price = 0
        services = db_bot.select_services()
        for service in services:
            if direction == (service.get('service_name')):
                ticket_price = int(service.get('service_price'))
                total_price = ticket_price*int(persons)



        
        await message.answer(f'Направление: <b>{direction}</b>, \nДата отправления: <b>{date}</b>, \nМест: <b>{persons}</b> , \nКонтакты: <b>{contact}</b> \n https://t.me/{contact} \n\nЦена билета: <b>{ticket_price} грн.</b>\nИтого: <b>{total_price}</b> грн.', reply_markup=ReplyKeyboardRemove())
        insert_result = db_bot.insert_order(tg_id=message.from_user.id, name=message.from_user.full_name, phone=contact, passagers=persons, route_datetime=date, route_direction=direction)
        if insert_result:
            await bot.send_message(ADMIN, 'Успешно добавлен заказ в базу')
        else:
            await bot.send_message(ADMIN, 'Не добавлен заказ в базу, сейчас вышлю сюда')
            await bot.send_message(ADMIN, f'Направление: <b>{direction}</b>, \nДата отправления: <b>{date}</b>, \nМест: <b>{persons}</b> , \nКонтакты: <b>{contact}</b> \n https://t.me/{contact} \n\nЦена билета: <b>{ticket_price} грн.</b>\nИтого: <b>{total_price}</b> грн.')

        await state.clear()
    else:
        keyboard_builder = ReplyKeyboardBuilder()#Создаем объект билдера кнопок
        keyboard_builder.button(text='Вернуться к вводу') #далее создаем кнопки
        await message.answer('Неверное колиечство', 
                                    reply_markup=keyboard_builder.as_markup(resize_keyboard=True, #Указываем настройки клавиатуры
                                    one_time_leyboard=True,
                                    input_field_placeholder=''                               
                                    ))
        await state.set_state(StepsForm.GET_PERSONS)





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
    dp.message.register(get_contact, StepsForm.GET_CONTACT)         #После введении имени переходим в функцию которая
    dp.message.register(get_persons, StepsForm.GET_PERSONS)         #После введении имени переходим в функцию которая
    dp.message.register(confirm_booking, StepsForm.CONFIRM_BOOKING)         #После введении имени переходим в функцию которая




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


