CREATE DATABASE bus TEMPLATE template0 ENCODING 'UTF8' LC_COLLATE 'en_US.utf8' LC_CTYPE 'en_US.utf8';
CREATE USER ticket WITH PASSWORD 'driving';
ALTER USER ticket WITH SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE bus TO ticket;




CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    tg_id TEXT,
    name TEXT,
    first_call TIMESTAMP,
    status TEXT,
    orders INTEGER
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    tg_id TEXT,
    name TEXT,
    phone TEXT,
    passagers INT,
    order_datetime TIMESTAMP,
    route_datetime TIMESTAMP,
    route_direction TEXT,
    route_id INTEGER,
    price DECIMAL,
    total_price DECIMAL,
    order_status TEXT
);

CREATE TABLE IF NOT EXISTS services(
    id SERIAL PRIMARY KEY,
    service_name TEXT,
    service_price DECIMAL,
    week_days TEXT,
    start_city INT,
    route_num INT
);

CREATE TABLE IF NOT EXISTS start_time(
    id SERIAL PRIMARY KEY,
    start_city INT,
    service_day TEXT,
    service_time TEXT
);


INSERT INTO start_time(start_city, service_day, service_time) VALUES
('1','','05:45'),
('1','','09:40'),
('1','','11:45'),
('1','','23:30'),
('2','','09:40'),
('2','','11:45'),
('2','','23:30'),
('3','','07:00'), --Одесса -Отопень - Бухарест
('3','','19:00'), --Одесса -Отопень - Бухарест
('4','','07:00'), -- Одесса - Констанца
('4','','11:00'), -- Одесса - Констанца
('4','','20:00'), -- Одесса - Констанца
('23','','15:00'), -- Исакча - Констанца
('23','','18:00'), -- Исакча - Констанца
('6','2','07:00'),
('6','4','17:30'),
('6','5','19:00'),
('7','3','07:30'),
('7','6','07:30'),



('8','','11:30'),
('8','','13:30'),
('8','','20:00'),
('8','','22:40'),
('9','','06:05'),
('9','','18:30'),
('9','','20:30'),
('10','','06:00'), --Отопень Одесса
('10','','20:00'), --Отопень Одесса
('24','','07:00'), --Бухарест Одесса
('24','','21:00'), --Бухарест Одесса
('11','','00:30'), --Орловка Одесса
('11','','13:00'), --Орловка Одесса
('12','','7:00'), --Констанца - Мамая -Одесса
('12','','17:00'), --Констанца - Мамая -Одесса
('13','','11:00'), --Исакча Одесса
('13','','21:00'), --Исакча Одесса
('14','','08:00'), --Констанца Исакча
('14','','18:00'), --Констанца Исакча
('15','4','14:00'), --Брашов Одесса
('15','6','12:00'), --Брашов Одесса
('15','0','14:00'), --Брашов Одесса

('17','6','10:00'), --Тимишора Одесса
('18','2','17:10'), --Люблин Одесса
('18','6','17:10'), --Люблин Одесса
('19','6','14:30'), --Варшава Одесса
('19','2','14:30'), --Варшава Одесса
('20','2','12:30'), --Лодзь Одесса
('20','6','12:30'), --Лодзь Одесса
('21','2','9:30'), --Познань Одесса
('21','6','9:30'), --Познань Одесса
('22','2','6:00'), --Щецин Одесса
('22','6','6:00'); --Щецин Одесса







INSERT INTO services(service_name,  service_price, week_days, start_city, route_num) VALUES
('Одесса - Кишинев', 900, '','1', '1'),
('Одесса - Яссы', 1700, '','2','2'),
('Одесса - Бухарест', 1600, '','3','3'),
('Одесса - Отопени Аэропорт', 1800, '','3','3'),
('Одесса - Орловка', 800, '','4','4'),
('Одесса - Констанца - Мамая', 1300, '','4','4'),
('Одесса - Ісакча', 1000, '','4','4'),
('Ісакча - Констанца', 800, '','23','4'),
('Одесса - Брашов', 2500, '2,4,5','6','5'),
('Одесса - Тимишоара', 3700, '4','6','5'),
('Одесса - Люблин', 1500, '3,6','7','6'),
('Одесса - Варшава', 1600, '3,6','7','6'),
('Одесса - Лодзь', 1900, '3,6','7','6'),
('Одесса - Познань', 2300, '3,6','7','6'),
('Одесса - Щецин', 4000, '3,6','7','6'),


('Кишинев - Одесса', 900, '','8','7'),
('Яссы - Одесса', 1700, '','9','8'),
('Отопени Аэропорт -  Одесса', 1800, '','10','9'),
('Бухарест - Одесса', 1600, '','24','9'),
('Орловка - Одесса', 800, '','11','10'),
('Констанца - Мамая - Одесса', 1300, '','12','10'),
('Ісакча - Одесса', 1000, '','13','10'),
('Констанца - Ісакча', 800, '','14','10'),
('Брашов - Одесса', 2500, '4,6,0','15','11'),
('Тимишоара - Одесса', 3700, '6','17','11'),
('Люблин - Одесса', 1500, '2,6','18','12'),
('Варшава  - Одесса', 1600, '2,6','19','12'),
('Лодзь - Одесса', 1900, '2,6','20','12'),
('Познань - Одесса', 2300, '2,6','21','12'),
('Щецин - Одесса', 4000, '2,6','22','12');



