CREATE DATABASE PlanB;

USE PlanB;

CREATE TABLE users {
    id BIGINT NOT NULL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    login VARCHAR(64) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(128) NOT NULL
}