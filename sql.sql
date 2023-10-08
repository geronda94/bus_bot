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
    week_days TEXT
);



INSERT INTO services(service_name,  service_price, week_days) VALUES
('Одесса - Кишинев', 800, ''),
('Одесса - Яссы', 1700, ''),
('Одесса - Бухарест ', 1600, ''),
('Одесса - Отопени Аэропорт', 1800, ''),
('Одесса - Орловка', 800, ''),
('Одесса - Констанца - Мамая', 1300, ''),
('Одесса - Ісакча', 1000, ''),
('Ісакча - Констанца', 800, ''),
('Одесса - Брашов', 2500, '1,4,5'),
('Одесса - Сибиу', 3000, '1,4,5'),
('Одесса - Тимишоара', 3700, '1,4,5'),
('Одесса - Люблин', 1500, '3,6'),
('Одесса - Варшава', 1600, '3,6'),
('Одесса - Лодзь', 1900, '3,6'),
('Одесса - Познань', 2300, '3,6'),
('Одесса - Щецин', 4000, '3,6'),


('Кишинев - Одесса', 800, ''),
('Яссы - Одесса', 1700, ''),
('Отопени Аэропорт -  Одесса', 1800, ''),
('Бухарест - Одесса', 1600, ''),
('Орловка - Одесса', 800, ''),
('Констанца - Мамая - Одесса', 1300, ''),
('Ісакча - Одесса', 1000, ''),
('Констанца - Ісакча', 800, ''),
('Брашов - Одесса', 2500, '1,4,5'),
('Сибиу - Одесса', 3000, '1,4,5'),
('Тимишоара - Одесса', 3700, '1,4,5'),
('Люблин - Одесса', 1500, '3,6'),
('Варшава  - Одесса', 1600, '3,6'),
('Лодзь - Одесса', 1900, '3,6'),
('Познань - Одесса', 2300, '3,6'),
('Щецин - Одесса', 4000, '3,6');



