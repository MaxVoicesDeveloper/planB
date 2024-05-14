-- Перед запуском удаляем старую БД и создаем новую

DROP DATABASE PlanBApp;

CREATE DATABASE PlanBApp;

USE PlanBApp;

-- Изменяю именование объектов, пишу с приставками (таблицы - 't_', индексы - 'idx_', представления - 'v_')
-- Таблица пользователей
CREATE TABLE t_users (
    id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    login VARCHAR(64) NOT NULL,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(128) NOT NULL,
    last_name VARCHAR(75) NOT NULL,
    first_name VARCHAR(75) NOT NULL,
    second_name VARCHAR(75),
    id_user_role BIGINT NOT NULL
);

-- Таблица задач
CREATE TABLE t_tasks (
    id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    desc_text TEXT,
    date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_deadline TIMESTAMP,
    id_executor BIGINT,
    id_status BIGINT NOT NULL
);

-- Таблица статусов задачи (справочник)
CREATE TABLE t_task_statuses (
    id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    status_code VARCHAR(50) NOT NULL,
    status_name VARCHAR(100) NOT NULL
);

-- Таблица ролей пользователь (справочник)
CREATE TABLE t_user_roles (
    id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    role_code VARCHAR(50) NOT NULL,
    role_name VARCHAR(100) NOT NULL
);