-- Перед запуском удаляем старую БД и создаем новую

DROP DATABASE PlanBApp;
CREATE DATABASE PlanBApp;

USE PlanBApp;

-- Создание пользователя приложения
CREATE USER 'app_user' IDENTIFIED BY 'app_user';
GRANT ALL PRIVILEGES ON *.* TO 'app_user' WITH GRANT OPTION;
FLUSH PRIVILEGES; 

-------------------------------------------------
-- Таблицы
-------------------------------------------------

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;


-- Таблица чатов
CREATE TABLE IF NOT EXISTS `t_chats` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Таблица сообщений чатов
CREATE TABLE IF NOT EXISTS `t_chat_messages` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_user` bigint NOT NULL,
  `id_chat` bigint NOT NULL,
  `date_sended` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `message_text` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_id_chat_idx` (`id_chat`),
  KEY `fk_id_user_idx` (`id_user`),
  CONSTRAINT `fk_id_chat` FOREIGN KEY (`id_chat`) REFERENCES `t_chats` (`id`),
  CONSTRAINT `fk_id_user` FOREIGN KEY (`id_user`) REFERENCES `t_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Таблица задач
CREATE TABLE IF NOT EXISTS `t_tasks` (
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;;


-- Таблица статусов задачи (справочник)
CREATE TABLE IF NOT EXISTS `t_task_statuses` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_code` varchar(50) NOT NULL,
  `status_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Таблица ролей пользователей (справочник)
CREATE TABLE `t_user_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_code` varchar(45) NOT NULL,
  `role_name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `role_code_UNIQUE` (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Справочная информация
INSERT INTO t_task_statuses(status_code, status_name)
VALUES ('NEW', 'Открыта'),
       ('CLOSED', 'Выполнена'),
       ('DELETED', 'Удалена');

INSERT INTO t_user_roles(role_code, role_name)
VALUES ('employer', 'Работодатель'),
       ('employee', 'Работник');


-------------------------------------------------
-- Функции
-------------------------------------------------

-- Функция создания нового сообщения (глобальный чат)
-- Args: p_id_user      - ID текущего пользователя
--       p_message_text - текстовое сообщение   
DELIMITER $$
CREATE DEFINER=`root`@`localhost` 
FUNCTION IF NOT EXISTS `f_create_new_message`(p_id_user      BIGINT,
								              p_message_text TEXT) RETURNS bigint
    DETERMINISTIC
BEGIN
	DECLARE l_id_message BIGINT;
    
	INSERT INTO t_chat_messages(id_user, id_chat, message_text)
    VALUES (p_id_user, 1, p_message_text);
    
    SELECT id INTO l_id_message FROM t_chat_messages WHERE id_user = p_id_user ORDER BY id DESC LIMIT 1;
RETURN l_id_message;
END$$
DELIMITER ;

-- Функция создания новой задачи
-- Args: p_id_user     - ID текущего пользователя
--       p_title       - имя задачи (заголовок)
--       p_desc_text   - текстовое описание (опционально - передается NULL (None))
--       p_id_executor - ID пользователя-исполнителя задачи (опционально)
--       p_deadline    - ДАТА конечного срока исполнения задачи (опционально)
--       p_id_fk       - ID родительской задачи (опционально)
DELIMITER $$
CREATE DEFINER=`root`@`localhost` 
FUNCTION IF NOT EXISTS `f_create_new_task`(p_id_user     BIGINT,
						        		   p_title       TEXT,
									       p_desc_text   TEXT,
                                           p_id_executor BIGINT,
                                           p_deadline    DATE,
                                           p_id_fk       BIGINT) RETURNS bigint
    DETERMINISTIC
BEGIN
	DECLARE l_id_task BIGINT;
    
    INSERT INTO t_tasks(title, desc_text, date_deadline, id_executor, id_fk, created_by)
    VALUES (p_title, p_desc_text, p_deadline, p_id_executor, p_id_fk, p_id_user);
    
    SELECT id INTO l_id_task FROM t_tasks WHERE created_by = p_id_user ORDER BY id DESC LIMIT 1;
RETURN l_id_task;
END$$
DELIMITER ;

-- Функция создания новой организации
DELIMITER $$
CREATE DEFINER=`root`@`localhost` 
FUNCTION IF NOT EXISTS `f_create_organization`(p_org_name  TEXT,
										                           p_org_desc  TEXT,
                                               p_org_num   TEXT,
                                               p_org_email TEXT,
                                               p_org_image BLOB,
                                               p_id_creator INTEGER) RETURNS int
    DETERMINISTIC
BEGIN
	DECLARE l_id_org INTEGER;
    
    INSERT INTO t_organzation(org_name, org_desc, legal_num, legal_email, image, created_by)
    VALUES (p_org_name, p_org_desc, p_org_num, p_org_email, p_org_image, p_id_creator);
    
    SELECT id INTO l_id_org
    FROM t_organization
    WHERE created_by = p_id_creator
    ORDER BY id DESC;
    
    UPDATE t_users
    SET id_org = l_id_org
    WHERE id = p_id_creator;
    
RETURN l_id_org;
END$$
DELIMITER ;

