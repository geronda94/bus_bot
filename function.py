def number_validator(number: str):
    if number:
        new_number = ''
        for i in range(len(number)):
            if number[i].isdigit():
                new_number += number[i]

            else:
                return False

        if 9 >= len(new_number) or len(new_number) <= 15:

            if  len(new_number) == 9 and new_number[0] != '0':
                new_number = '0'+new_number
                return new_number

            elif len(new_number) == 10 and new_number[0] == '0':
                return new_number


        else:
            return False
    else:
        return False