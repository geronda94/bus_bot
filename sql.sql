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
    order_datetime TIMESTAMP,
    route_datetime TIMESTAMP,
    route_direction TEXT,
    route_id INTEGER
);

CREATE TABLE IF NOT EXISTS services(
    id SERIAL PRIMARY KEY,
    service_name TEXT,
    service_desc TEXT,
    service_price DECIMAL,
    start_city TEXT,
    finish_city TEXT
);



INSERT INTO services(service_name, service_desc, service_price, start_city, finish_city) VALUES
('Одесса - Бухарест', 'Одесса - Кишинев - Яссы - Бухарест', 1050, 'Одесса', 'Бухарест'),
('Одесса - Констанца', 'Одесса - Кишинев - Констанца - Наводари', 1500, 'Одесса', 'Наводари'),
('Одесса - София', 'Одесса - Кишинев - Констанца - София', 1700, 'Одесса', 'София'),
('София - Одесса', 'Одесса - Кишинев - Констанца - София', 1700, 'София', 'Одесса'),
('Констанца - Одесса', 'Одесса - Кишинев - Констанца - София', 1700, 'Констанца', 'Одесса'),
('Бухарест - Одесса', 'Одесса - Кишинев - Констанца - София', 1700, 'Бухарест', 'Одесса'),
;


