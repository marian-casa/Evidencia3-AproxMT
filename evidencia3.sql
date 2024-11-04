-- Codigo para la creacion de la Base de datos

CREATE DATABASE sensor_data;
USE sensor_data;
CREATE TABLE dht22_data (
id INT AUTO_INCREMENT PRIMARY KEY,
temperatura FLOAT NOT NULL,
humedad FLOAT NOT NULL,
timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seleccionar los elemntos de la base de datos
SELECT * FROM dht22_data