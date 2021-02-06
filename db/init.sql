-- database create DDL
CREATE DATABASE final_project_db;
use final_project_db;

-- table create DDL
/*CREATE TABLE IF NOT EXISTS app_roles (
    `id` INT AUTO_INCREMENT,
    `code` VARCHAR(5) CHARACTER SET utf8,
    `description` VARCHAR(50) CHARACTER SET utf8,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS user_type (
    `id` INT AUTO_INCREMENT,
    `code` VARCHAR(5) CHARACTER SET utf8,
    `description` VARCHAR(50) CHARACTER SET utf8,
    PRIMARY KEY (`id`)
);
*/
CREATE TABLE IF NOT EXISTS user_status (
    `id` INT AUTO_INCREMENT,
    `code` VARCHAR(5) CHARACTER SET utf8,
    `description` VARCHAR(50) CHARACTER SET utf8,
    PRIMARY KEY (`id`)
);
/*
CREATE TABLE IF NOT EXISTS user_address (
    `id` INT AUTO_INCREMENT,
    `type` VARCHAR(10) CHARACTER SET utf8,
    `line_1` VARCHAR(50) CHARACTER SET utf8,
    `line_2` VARCHAR(50) CHARACTER SET utf8,
    `city` VARCHAR(25) CHARACTER SET utf8,
    `state` VARCHAR(25) CHARACTER SET utf8,
    `zip_code` VARCHAR(10) CHARACTER SET utf8,
    `email` VARCHAR(100) CHARACTER SET utf8,
    `phone` VARCHAR(10) CHARACTER SET utf8,
    PRIMARY KEY (`id`)
);
*/

CREATE TABLE IF NOT EXISTS app_users (
    `id` INT AUTO_INCREMENT,
    `email` VARCHAR(100) CHARACTER SET utf8 not null ,
    `password` VARCHAR(25) CHARACTER SET utf8 not null ,
    `first_name` VARCHAR(50) CHARACTER SET utf8 not null ,
    `last_name` VARCHAR(50) CHARACTER SET utf8 not null ,
    `phone` VARCHAR(10) CHARACTER SET utf8,
    /*`role_id` INT not null references app_roles(id) ,*/
    /*`type_id` INT not null references user_type(id) ,*/
    `status_id` INT not null references user_status(id) ,
    `confirmed` INT DEFAULT 0,
    `confirmed_on` TIMESTAMP NULL DEFAULT NULL,
    `created_on` TIMESTAMP NULL DEFAULT NULL,
    `updated_on` TIMESTAMP NULL DEFAULT NULL,
    /*`address_id` INT not null references user_address(id),*/
    PRIMARY KEY (`id`)
);

-- data population DML for 100 records

INSERT INTO user_status VALUES
    (1,'A','Active'),
    (2,'I','Inactive')
 ;
/*
INSERT INTO user_type VALUES
    (1,'U','Regular User'),
    (2,'A','Admin'),
    (3,'S','Support')
 ;

INSERT INTO app_roles VALUES
    (1,'U','Regular User'),
    (2,'A','Admin'),
    (3,'S','Support')
 ;*/

 /* Calendar Database scripts */

CREATE TABLE IF NOT EXISTS events (
    `id` int AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL ,
    `start_event` datetime NOT NULL,
    `end_event` datetime NOT NULL,
    `event_id` VARCHAR(255) ,
    PRIMARY KEY (`id`)
);
INSERT INTO events(title,start_event,end_event,event_id) VALUES
    ('Hike','2020-12-10 13:00:00','2020-12-10 15:59:59','sacsdjk123'),
    ('Travel','2020-12-13 13:00:00','2020-12-13 15:59:59','');