
INSERT INTO unit (name, symbol) VALUES ('Humedad relativa', '% RH');
INSERT INTO unit (name, symbol) VALUES ('Temperatura', 'ºC');
INSERT INTO unit (name, symbol) VALUES ('Humedad del suelo', '?');
INSERT INTO unit (name, symbol, highest, lowest) VALUES ('Luz', '%', 100, 0);

INSERT INTO sensor (model, unit) VALUES ('DHT22', 1);
INSERT INTO sensor (model, unit) VALUES ('DHT22', 2);
INSERT INTO sensor (model, unit) VALUES ('Soil Moisture Probe', 3);
INSERT INTO sensor (model, unit) VALUES ('LDR', 4);

INSERT INTO plant (name, fase1, fase2, fase3, fase4) VALUES ('Helecho', 1, 2, 3, 4);

INSERT INTO user (email, password, name) VALUES ('example@example.org', SHA2('example1234',256), 'Example');
INSERT INTO field (user) VALUES ('example@example.org');
INSERT INTO area (field, sensor_hum, sensor_tem, sensor_moi, sensor_lig) VALUES (1, 1, 2, 3, 4);

INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:00:00', 21, 24.20, 38.40, 500);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:05:00', 15, 23.60, 36.70, 558);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:10:00', 13, 23.80, 38.00, 557);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:15:00', 15, 22.60, 39.30, 560);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:20:00', 21, 24.20, 38.40, 500);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:25:00', 0, 21.90, 39.50, 559);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:30:00', 0, 21.60, 40.00, 559);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:35:00', 15, 22.40, 40.70, 551);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:40:00', 17, 22.90, 40.90, 550);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:45:00', 17, 23.40, 41.30, 552);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:50:00', 20, 24.10, 40.00, 552);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 14:55:00', 21, 24.20, 38.40, 500);
INSERT INTO env (area, dat, lightness, temperature, humidity, moisture) VALUES (1, '2019-04-01 15:00:00', 22, 24.10, 37.80, 556);