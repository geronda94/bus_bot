from datetime import datetime
import re
import psycopg2
from psycopg2 import pool
from config import DB
import math
import re

from function import week_days_name




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






class BotDB:
    def __init__(self, request: PgRequest):
        self.__request = request

    def select_services(self):
        return self.__request.selectd('SELECT * FROM services;')
    
    def insert_order(self, tg_id, name, phone, passagers, route_datetime, route_direction, price, total_price):
        try:
            self.__request.insert('INSERT INTO orders(tg_id, name, phone, passagers, order_datetime, route_datetime, route_direction, order_status, price, total_price) VALUES(%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)', 
                                  (tg_id, name, phone, passagers, datetime_now(), route_datetime, route_direction, 'posted', price, total_price))
            return True
        except Exception as ex:
            print(ex)
            return False
        
    def select_new_orders(self):
        return self.__request.selectd('SELECT * FROM orders WHERE order_status = %s',('posted',))
    
    def set_order_status(self, order_id, order_status):
        try:
            self.__request.insert('UPDATE orders SET order_status = %s WHERE id = %s', (str(order_status), str(order_id)))
            return True
            
        except Exception as ex:

            return False
    
    def get_user_orders(self, user_id):
        try:
            orders = self.__request.selectd('SELECT * FROM orders WHERE tg_id = %s;',(str(user_id),))
            return orders
        except Exception as ex:
            print(ex)
            return False
        

    def select_clock(self, route, wday=''):        
        query = "SELECT * FROM start_time WHERE start_city = %s;"
        try:
            res = self.__request.selectd(query, (route,))
            
            if res[0].get('service_day') == '':
                return res
            else:
                lst = []
                for i in res:
                    if i.get('service_day') == str(wday):
                        lst.append(i)

                if len(lst) >0:
                    return lst
                else:
                    return []
        except Exception as ex:
            print(ex)
            return []
        
    def get_start_clock(self, start_city):
        query = "SELECT * FROM start_time WHERE start_city = %s;"
        try:
            res = self.__request.selectd(query, (start_city,))
            return res
        except Exception as ex:
            return []

connect = PgConnect(host=DB.host, port=DB.port, database=DB.database, user=DB.user, password=DB.password)
request_db = PgRequest(connect)

db_bot = BotDB(request_db)





start_time = db_bot.get_start_clock('1')


schedule =''
schedule_days = {x.get('service_day'):'' for x in start_time}
for i in start_time:
    schedule_days[i.get('service_day')] += i.get('service_time') +' '


numer = 0
for key, val in schedule_days.items():
    numer +=1
    sep = ''
    if numer == len(schedule_days):
        sep = '| '
    schedule+= f'{week_days_name(key)} {val}'+ sep

