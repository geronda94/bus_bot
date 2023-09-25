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
    




connect = PgConnect(host=DB.host, port=DB.port, database=DB.database, user=DB.user, password=DB.password)
request_db = PgRequest(connect)

db_bot = BotDB(request_db)


