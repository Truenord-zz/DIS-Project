DROP TABLE IF EXISTS Users CASCADE;

CREATE TABLE IF NOT EXISTS Users(
	pk serial not null PRIMARY KEY,
	user_name varchar(50) UNIQUE,
    full_name varchar(50),
	password varchar(120)
);

CREATE INDEX IF NOT EXISTS users_index
ON Users (pk, user_name);

DELETE FROM Users;

DROP TABLE IF EXISTS Pharmacists;

CREATE TABLE IF NOT EXISTS Pharmacists(
    PRIMARY KEY(pk)
) INHERITS (Users);

CREATE INDEX IF NOT EXISTS pharmacists_index
ON Pharmacists(pk, user_name);

DELETE FROM Pharmacists;

INSERT INTO Pharmacists(user_name, full_name, password)
VALUES ('pharmacist', 'Pharmacist', 'pass');

DROP TABLE IF EXISTS Customers;

CREATE TABLE IF NOT EXISTS Customers(
    PRIMARY KEY(pk)
) INHERITS (Users);

CREATE INDEX IF NOT EXISTS customers_index
ON Customers (pk, user_name);

DELETE FROM Customers;

INSERT INTO Customers(user_name, full_name, password)
VALUES ('customer', 'Customer', 'pass');