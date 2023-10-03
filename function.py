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




def get_days():
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



   # Получаем текущую дату
    today = datetime.date.today()
    this_month = today.month
    
    # Получаем первый день следующего месяца
    first_day_of_next_month = today.replace(day=1, month=today.month + 1 if today.month!=12 else 1)
    if today.month == 12:
        first_day_of_next_month = first_day_of_next_month.replace(year=today.year + 1, month=1)

    # Вычисляем последний день текущего месяца
    last_day_of_current_month = first_day_of_next_month - datetime.timedelta(days=1)

    # Создаем список дней, оставшихся в текущем месяце
    remaining_days = [(today + datetime.timedelta(days=i)).strftime('%d/%m') for i in range((last_day_of_current_month - today).days + 1)]

    # Формируем список дней текущего месяца
    this_month_days = []
    for day in remaining_days:
        this_month_days.append(str(day))
    


    # Получаем название следующего месяца
    next_month = first_day_of_next_month.month
    last_day_of_next_month = first_day_of_next_month.replace(day=1) - datetime.timedelta(days=1)
    # Создаем список дней следующего месяца
    next_month_days = []
    current_day = first_day_of_next_month
    while current_day.month == first_day_of_next_month.month:
        next_month_days.append(str(current_day.strftime('%d/%m')))
        current_day += datetime.timedelta(days=1)

    months = {
        months_name.get(str(this_month)): this_month_days,
        months_name.get(str(next_month)): next_month_days
    }

    return months

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
    

