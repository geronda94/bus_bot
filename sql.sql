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
    order_status TEXT
);

CREATE TABLE IF NOT EXISTS services(
    id SERIAL PRIMARY KEY,
    service_name TEXT,
    service_price DECIMAL,
    week_days TEXT
);



INSERT INTO services(service_name,  service_price, week_days) VALUES
('Одесса - Констанца - Мамая', 1050, ''),
('Одесса - Бухарест - Отопени', 1050, ''),
('Одесса - Кишинев', 1050, ''),
('Одесса - Яссы', 1050, ''),
('Одесса - Брашов - Сибиу', 1050, '1,4,5'),
('Одесса - Люблин - Варшава - Лодзь - Познань - Цецен', 1050, '3,6'),

('Мамая - Констанца - Одесса', 1050, ''),
('Отопени - Бухарест - Одесса', 1050, ''),
('Кишинев - Одесса', 1050, ''),
('Яссы - Одесса', 1050, ''),
('Сибиу - Брашов - Одесса', 1050, '4,6,7'),
('Цецен - Познань - Лодзь - Варшава - Люблин - Одесса', 1050, '2,6');




