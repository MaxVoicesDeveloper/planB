-- Перед запуском удаляем старую БД и создаем новую

DROP DATABASE PlanBApp;

CREATE DATABASE PlanBApp;

USE PlanBApp;

-- Изменяю именование объектов, пишу с приставками (таблицы - 't_', индексы - 'idx_', представления - 'v_', внешние ключи - 'fk_')
-- Таблица пользователей
CREATE TABLE `t_users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `login` varchar(64) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(128) NOT NULL,
  `last_name` varchar(75) NOT NULL,
  `first_name` varchar(75) NOT NULL,
  `second_name` varchar(75) DEFAULT NULL,
  `account_type` varchar(25) NOT NULL DEFAULT 'employee',
  PRIMARY KEY (`id`)
);


-- Таблица задач
CREATE TABLE `t_tasks` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `desc_text` text,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_deadline` timestamp NULL DEFAULT NULL,
  `id_executor` bigint DEFAULT NULL,
  `id_status` bigint NOT NULL,
  `id_fk` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_id_executor_idx` (`id_executor`),
  KEY `fk_id_status_idx` (`id_status`),
  CONSTRAINT `fk_id_executor` FOREIGN KEY (`id_executor`) REFERENCES `t_users` (`id`),
  CONSTRAINT `fk_id_status` FOREIGN KEY (`id_status`) REFERENCES `t_task_statuses` (`id`)
);


-- Таблица статусов задачи (справочник)
CREATE TABLE `t_task_statuses` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_code` varchar(50) NOT NULL,
  `status_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
);

-- Справочная информация
INSERT INTO t_task_statuses(status_code, status_name)
VALUES ('NEW', 'Открыта'),
       ('CLOSED', 'Выполнена'),
       ('DELETED', 'Удалена');
