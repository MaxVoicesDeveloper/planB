CREATE DATABASE PlanBApp;
USE PlanBApp;
CREATE TABLE `t_users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `login` varchar(64) NOT NULL,
  `password` varchar(50) NOT NULL,
  `email` varchar(128) NOT NULL,
  `last_name` varchar(75) NOT NULL,
  `first_name` varchar(75) NOT NULL,
  `second_name` varchar(75) DEFAULT NULL,
  `id_org` bigint DEFAULT NULL,
  `account_type` varchar(25) NOT NULL DEFAULT 'employee',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `t_chats` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Таблица сообщений чатов
CREATE TABLE `t_chat_messages` (
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

CREATE TABLE IF NOT EXISTS `t_task_statuses` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_code` varchar(50) NOT NULL,
  `status_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO t_task_statuses(status_code, status_name)
VALUES ('NEW', 'Открыта'),
       ('CLOSED', 'Выполнена'),
       ('DELETED', 'Удалена');

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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `t_user_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_code` varchar(45) NOT NULL,
  `role_name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `role_code_UNIQUE` (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO t_user_roles(role_code, role_name)
VALUES ('employer', 'Работодатель'),
       ('employee', 'Работник');


CREATE TABLE `t_organization` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `org_name` varchar(100) NOT NULL,
  `org_desc` varchar(1000) DEFAULT NULL,
  `legal_num` varchar(16) NOT NULL,
  `legal_email` varchar(75) NOT NULL,
  `created_by` bigint NOT NULL,
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `org_name_UNIQUE` (`org_name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;



CREATE TABLE `t_invitations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `from_user_id` bigint NOT NULL, -- ID работодателя
  `to_user_id` bigint NOT NULL, -- ID работника
  `organization_id` bigint NOT NULL, -- ID организации
  `status` enum('pending', 'accepted', 'declined') NOT NULL DEFAULT 'pending', -- Статус заявки
  `date_sent` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Дата отправки
  PRIMARY KEY (`id`),
  FOREIGN KEY (`from_user_id`) REFERENCES `t_users`(`id`),
  FOREIGN KEY (`to_user_id`) REFERENCES `t_users`(`id`),
  FOREIGN KEY (`organization_id`) REFERENCES `t_organization`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


ALTER TABLE t_users ADD COLUMN profession VARCHAR(255) DEFAULT 'Unknown';

ALTER TABLE t_tasks MODIFY COLUMN id_status bigint NOT NULL DEFAULT 1;