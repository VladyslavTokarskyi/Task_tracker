# Task_tracker

Hello everyone, this is a task tracking app where you can create and manage your own to-do lists.  
The app includes user authentication with login, sign-up, and account deletion options.

You can create tasks with deadlines and priority levels, and tasks change color based on their priority.  
Tasks can also be marked as completed.

The app supports both German and English languages and offers light and dark themes.

This project is also hosted on vladyslavtokarskyi.de if you want to try it without having to set up a database and virtual environment yourself.

# Get started

1. Create a virtual environment and install `requirements.txt`.

   **Important note:** `flask-mysqldb` is stable only on Python 3.7–3.11.  
   If you wish to use a newer Python version, use an alternative like **PyMySQL**, but you will need to make changes in the code.

2. Create a database in MySQL with:

```sql
CREATE TABLE users (
    userid INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255),
    password VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (userid),
    UNIQUE KEY username (username)
);

CREATE TABLE user_settings (
    userid INT PRIMARY KEY,
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
);```
3. In the `.env` file configure your database like this:

```env
MYSQL_HOST=sql_host
MYSQL_USER=sql_user
MYSQL_PASSWORD=your_password
MYSQL_DB=database_name
FLASK_SECRET_KEY=secret_key
```

4. you can start using it

