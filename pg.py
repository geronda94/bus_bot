from datetime import datetime
import re
import psycopg2
from psycopg2 import pool
from config import DB
import math
import re




def time():
    return datetime.now().strftime('%H:%M:%S')

def today():
    return datetime.now().strftime('%Y-%m-%d')

def datetime_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #return datetime.now().strftime('%d-%m-%Y %H:%M:%S')


def error_log(ex):
    with open('error.txt', 'a') as error_file:
                error_file.write(f'Ошибка: {str(ex)}\n')

def check_booking_date(date):
    if not date:
        return None
    else:
        if date[2] == '-':
            return str(date.split('-')[::-1])

        return str(date.split('-'))


def check_booking_time(time):
    if not time or len(time)!=5:
        return None
    else:
        return time



def services_filter(services_list, lang:str = 'ro'):
    new_list = []
    for i in services_list:
        s_id = i.get('id')
        order_num = i.get('order_num')
        service_link = i.get('service_link')
        service_name = i.get('service_name_'+lang)
        avatar_link = i.get('avatar_link')
        
        if i.get('service_li_'+lang):
            service_li = [x for x in i.get('service_li_'+lang).split(',')]
        else:
            service_li = None
        time_need = i.get('time_need')
        service_description = i.get('service_description_'+lang)

        #Блок по фильрации списка опций
        service_types = list()
        for key, val in i.items():
            filter_keys = []
            if 'type_' in str(key) and lang in str(key) and val is not None:
                type_num = key.split('_')[1]
                type_val = val
                # service_types.append({
                #     f'type_{type_num}_name':type_val,
                #     f'type_{type_num}_price':i.get(f'type_{type_num}_price')
                #     })
                service_types.append((type_val, float(i.get(f'type_{type_num}_price')),))
        
        new_list.append(
            {
                'service_id':s_id,
                'order_num':order_num,
                'service_link':service_link,
                'service_name':service_name,
                'avatar_link':avatar_link,
                'service_li':service_li,
                'time_need':time_need,
                'service_description':service_description,
                'service_types':service_types
            })
    return new_list


class PgConnect:
    def __init__(self, minconn=1, maxconn=10, **kwargs):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn, maxconn, **kwargs)

    def __enter__(self):
        self.conn = self.connection_pool.getconn()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.connection_pool.putconn(self.conn)

    def execute(self, sql, params=None):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchall()

    def push(self, sql, params=None):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql, params)


class PgRequest:
    def __init__(self, db: PgConnect):
        self.__db = db


    def execute(self, request, params=None):
        with self.__db as conn:
            with conn.cursor() as cur:
                cur.execute(request, params)
                return cur.fetchone()[0]



    def insert(self, request, params=None):
        with self.__db as conn:
            self.__db.push(request, params)

    def select(self, request, params=None):
        with self.__db as conn:
            return self.__db.execute(request, params)
        
    def selectd(self, request, params=None):
        with self.__db as conn:
            with conn.cursor() as cur:
                cur.execute(request, params)
                columns = [desc[0] for desc in cur.description]
                return [dict(zip(columns, row)) for row in cur.fetchall()]






class Services:
    def __init__(self, request: PgRequest):
        self.__request = request

    
    def get_services(self, lang: str = 'ro'):
        services = self.__request.selectd('SELECT * FROM services ORDER BY order_num;')
        return services_filter(services_list=services, lang=lang)
    

    def get_service(self, service_link: str, lang: str = 'ro') :
        service = self.__request.selectd('SELECT * FROM services WHERE service_link=%s;', (service_link,))
        return services_filter(services_list=service, lang=lang)
    
    
    def start_clients(self, phone:str, service_link:str, booking_date, 
                                service_name, sid, lang: str = 'ro'):
        
        booking_date = check_booking_date(booking_date)
        
        posted_date = datetime_now()        
        check_number = self.__request.select('SELECT client_phone FROM start_clients WHERE client_phone = %s', (phone,))
        
        if len(check_number) == 0:
            self.__request.insert('''INSERT INTO start_clients(client_phone, service_link, service_name, booking_date, order_posted, session_id )
                                                VALUES(%s,%s,%s,%s,%s,%s)''',
                                                (phone, service_link, service_name, booking_date, posted_date, sid,))
        

    def check_time(self, booking_date, time_need, lang: str = 'ro'):
        select_orders = self.__request('SELECT * FROM booking WHERE booking_date = %s', (booking_date,))






    def service_booking(self, sid, ip_address, booking_date, booking_time, client_phone, service_name, service_link,
                        service_price, car_type,  lang: str = 'ro'):
        
        posted_date = datetime_now()
        booking_date = check_booking_date(booking_date)
        
        booking_time = check_booking_time(booking_time)

        try:
            self.__request.insert('''INSERT INTO booking(session_id, ip_address, booking_date,
                                booking_time, client_phone, service_name, service_link,
                                service_price, car_type, order_posted, order_status, client_lang) 
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                    (sid, ip_address, booking_date, booking_time,client_phone, service_name,
                                    service_link, service_price, car_type, posted_date, 'posted', lang,))
            return True
        
        except Exception as ex:
            error_log(ex=ex)
            return False
        


    def check_new_orders(self):
        return self.__request.selectd('SELECT * FROM booking WHERE order_status = %s',('posted',))

    def set_booking_status(self, booking_id, booking_status):
        try:
            self.__request.insert('UPDATE booking SET order_status = %s WHERE id = %s', (booking_status, booking_id,))
            return True
        
        except Exception as ex:
            error_log(ex=ex)
            return False



class Static:
    def __init__(self, request: PgRequest):
        self.__request = request

    def select_slider(self, lang: str = 'ro'):
        items =  self.__request.selectd('SELECT * FROM slider ORDER BY order_by;')
        new_list = []

        for i in items:
            new_list.append({
                'id':i.get('id'),
                'photo_link':i.get('photo_link'),
                'photo_name':i.get('photo_name'),
                'order_by':i.get('order_by'),
                'title':i.get(f'title_{lang}'),
                'desc':i.get(f'desc_{lang}'),
                'color':i.get(f'color')
            })

        return new_list



class Users:
    def __init__(self, request: PgRequest):
        self.__request = request

    def get_user(self, user_id: str ):
        result = self.__request.selectd('SELECT * FROM users WHERE id = %s', (user_id,))[0]
        return result

    def user_for_login(self, login: str ):
        try:
            result = self.__request.selectd('SELECT * FROM users WHERE login = %s', (login,))[0]
            return result
        
        except Exception as ex:
            error_log(ex=ex)
            return False
    




connect = PgConnect(host=DB.host, port=DB.port, database=DB.database, user=DB.user, password=DB.password)
request_db = PgRequest(connect)

services = Services(request_db)
static = Static(request_db)
users = Users(request_db)

