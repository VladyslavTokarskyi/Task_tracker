CREATE DATABASE IF NOT EXISTS todo_database;

DROP TABLE users;

CREATE TABLE users (
    userid INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255),
    password VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (userid),
    UNIQUE KEY username (username)
);

DROP TABLE user_settings;

CREATE TABLE user_settings (
    userid INT PRIMARY KEY,
    theme ENUM('light', 'dark') NOT NULL DEFAULT 'light',
    language ENUM('en', 'de') NOT NULL DEFAULT 'en'
);

DROP TABLE tasks;

CREATE TABLE tasks (
    id INT NOT NULL AUTO_INCREMENT,
    task_text VARCHAR(255) NOT NULL,
    deadline DATE DEFAULT NULL,
    priority VARCHAR(255) DEFAULT NULL,
    status TINYINT(1) DEFAULT 0,
    userid INT NOT NULL,
    PRIMARY KEY (id),
    KEY userid (userid)
);
