import datetime


def number_validator(number: str):
    if number:
        new_number = ''
        for i in range(len(number)):
            if number[i].isdigit():
                new_number += number[i]

        if 8 <= len(new_number) and len(new_number) < 15:
            return new_number

        else:
            return False
    else:
        return False


def get_month_days(year, month):
    # Находим первый день месяца
    year = int(year)
    month = int(month)

    if month == datetime.datetime.now().month:
        first_day = datetime.datetime.now().date()
    else:
        first_day = datetime.date(year, month, 1)

    last_day = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
    days = [first_day + datetime.timedelta(days=x) for x in range((last_day - first_day).days + 1)]
    
    # Возвращаем список дней
    return days



def get_days(service_days: str =''):
    months_name = {
        '1':'Январь',
        '2':'Февраль',
        '3':'Март',
        '4':'Апрель',
        '5':'Май',
        '6':'Июнь',
        '7':'Июль',
        '8':'Август',
        '9':'Сентябрь',
        '10':'Октябрь',
        '11':'Ноябрь',
        '12':'Декабрь',
    }

    week_days_list = ['1','2','3','4','5','6','7']
    if service_days :
        week_days_list = [x for x in service_days.split(',')]


   # Получаем текущую дату
    today = datetime.date.today()
    this_month = today.month
    next_month = this_month+1 if this_month != 12 else 1
    this_year = today.year
    next_year = this_year+1
    next_month_year = this_year if next_month != 1 else next_year
    
    this_month_days = []
    next_month_days = []

    for i in get_month_days(this_year, this_month):
        if i.strftime('%w') in week_days_list:
            this_month_days.append(i.strftime('%d/%m'))

    for i in get_month_days(next_month_year, next_month):
        if i.strftime('%w') in week_days_list:
            next_month_days.append(i.strftime('%d/%m'))


    months = {
        months_name.get(str(this_month)): this_month_days,
        months_name.get(str(next_month)): next_month_days
    }

    return  months



# for key, val in get_days('').items():
#     print(key)
#     for j in val:
#         print(j)


def week_days_names(service_days: str =''):
    wdays = {
        '1':'Пн.',
        '2':'Вт.',
        '3':'Ср.',
        '4':'Чт.',
        '5':'Пт.',
        '6':'Сб.',
        '7':'Вс.'
    }

    names_list = ''


    if service_days != None and service_days != '':
        days_list = [str(x) for x in service_days.split(',')]
        for i in days_list:
            names_list = names_list + wdays.get(i) +' '
        return names_list

    else:
        return "Ежедневно"




def check_date_format(date: str):
    if len(date) == 5:
        for i in range(len(date)):
            if i != 2 and date[i].isdigit():
                continue
            elif i==2 and date[i] =='/':
                continue
            else:
                return False
        return True


    else:
        return False
    



def format_date(date: str):
    date_now = datetime.datetime.now()
    current_year = date_now.strftime('%Y')
    current_month = date_now.strftime('%m')


    recived_date = date.split('/')
    year = ''

    if current_month > recived_date[1]:
        year = str(int(current_year)+1)
    else:
        year = current_year
    
    new_date = f'{year}-{recived_date[1]}-{recived_date[0]}'
    return datetime.datetime.strptime(new_date, '%Y-%m-%d')






# days_list = get_days('').items()
# calendar_list = []

# for month_name, date_list in days_list:
#     calendar_list.append(month_name)            

#     date_list_buttons = []
#     count_days = 0
#     last_count = len(date_list) %5

#     for i in range(len(date_list)):
#         day = date_list[i]

#         date_list_buttons.append(day)
#         count_days +=1   

#         if count_days == 5:
#             calendar_list.append(date_list_buttons)
#             count_days = 0
#             date_list_buttons = []
#         if (len(date_list) - i < 5) and (last_count == count_days):
#             for i in range(5- len(date_list_buttons)):
#                 date_list_buttons.append(' ')
#             calendar_list.append(date_list_buttons)
#             count_days = 0
#             date_list_buttons = []



# for i in calendar_list:
#     print(i)


