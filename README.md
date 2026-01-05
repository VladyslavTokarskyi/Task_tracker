# Task_tracker
Hello everyone, this is a task tracking app where you can create and manage your own to-do lists. The app includes user authentication with login, sign-up, and account deletion options. You can create tasks with deadlines and priority levels, and tasks change color based on their priority. Tasks can also be marked as completed. The app supports both German and English languages and offers light and dark themes.

This project is also hosted on vladyslavtokarskyi.de if you want to try it without having to setup Database and virtual environment yourself.

# Get started
1. Create virtual environment and install requirments.txt. Important note! flask-mysqldb is stable only on python 3.7-3.11 .If you wish to use newer python version use other alternative "PyMySQl" but you will need to make changes in code.
2. Create database in MySQL with '''CREATE TABLE users (
    userid INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255),
    password VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (userid),
    UNIQUE KEY username (username)
);


CREATE TABLE user_settings (
    userid INT PRIMARY KEY ,
    theme ENUM('light', 'dark') NOT NULL DEFAULT 'light',
    language ENUM('en', 'de') NOT NULL DEFAULT 'en'
);


CREATE TABLE tasks (
    id INT NOT NULL AUTO_INCREMENT,
    task_text VARCHAR(255) NOT NULL,
    deadline DATE DEFAULT NULL,
    priority VARCHAR(255) DEFAULT NULL,
    status TINYINT(1) DEFAULT 0,
    userid INT NOT NULL,
    PRIMARY KEY (id),
    KEY userid (userid)
); '''




