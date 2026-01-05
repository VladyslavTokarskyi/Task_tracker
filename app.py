from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from dotenv import load_dotenv
import datetime
import secrets
import os
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()   



app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  
csrf = CSRFProtect(app)



# MySQL Config
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")


mysql = MySQL(app)

app.permanent_session_lifetime = timedelta(days=30)

SUPPORTED_LANGUAGES = ["en", "de"]
DEFAULT_LANG = "en"


def get_browser_language():
    return request.accept_languages.best_match(
        SUPPORTED_LANGUAGES) or DEFAULT_LANG


@app.before_request
def set_language():
    if "lang" not in session:
        session["lang"] = get_browser_language()


@app.context_processor
def inject_session_vars():
    return dict(
        session_username=session.get("username", ""),
        session_lang=session.get("lang", "en"),
        session_theme=session.get("theme", "light")
    )

@app.context_processor
def inject_csrf():
    return dict(csrf_token=generate_csrf)

def checklang(en, de):
    if session["lang"] == "en":
        message = en
    else:
        message = de
    return message


# //////////////////// Home page ///////////////////////
@app.route("/")
def index():
    return render_template("index.html",
                           lang=session.get("lang", "en"),
                           theme=session.get("theme", "light"))


# /////////////////////// Sign_up ///////////////////////
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    error = False
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        has_number = any(char.isdigit() for char in password)
        has_uppercase = any(char.isupper() for char in password)
        has_special = any(not char.isalnum() for char in password)

        cur = mysql.connection.cursor()
        cur.execute("SELECT userid FROM users WHERE username = %s",
                    (username,))
        user = cur.fetchone()

        if user:
            mysql.connection.commit()
            cur.close()
            error = True
            return render_template("sign_up.html", error=error,
                                   message=checklang("User already exists","Benutzer existiert bereits"))
        else:
            if len(password) >= 8 and has_number and has_uppercase and has_special:
                cur.execute(
                    "INSERT INTO users (username, password) VALUES (%s, %s)",
                    (username, hashed_password))
                userids = cur.lastrowid  
                
                cur.execute("INSERT INTO user_settings (userid) VALUES (%s)",
                            (userids,))
                mysql.connection.commit()
                cur.close()
                return redirect("/login")

            else:
                mysql.connection.commit()
                cur.close()
                error = True
                return render_template("sign_up.html", error=error,
                                       message=checklang("Password requires 8 chars, uppercase, symbol","Passwort benötigt 8 Zeichen, Großbuchst., Symbol   "))
    return render_template("sign_up.html")


# /////////////////////// Login ///////////////////////
@app.route("/login", methods=["GET", "POST"])
def login():
    error = False
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT userid,password FROM users WHERE username=%s ",
            (username,))
        user = cur.fetchone()
        

        if user and check_password_hash(user[1], password):

            if "remember" in request.form:
                session.permanent = True
            else:
                session.permanent = False

            session["userid"] = user[0]

            session["username"] = username

            cur.execute(
                "SELECT theme, language FROM user_settings WHERE userid = %s",
                (session["userid"],)
            )

            settings = cur.fetchone()

            if settings:
                session["theme"] = settings[0]
                session["lang"] = settings[1]
            else:
                session["lang"] = "en"

            cur.close()
            return redirect("/dashboard")
        else:
            error = True
            return render_template("login.html", error=error,
                                   message=checklang("Wrong username or password","Falscher Benutzername oder falsches Passwort"))

    return render_template("login.html")

# /////////////////////// Cancel delete ///////////////////////
@app.route("/cancel_delete")
def cancel_delete():
    session.pop("account_exists", None)
    session.pop("delete_userid", None)
    return redirect("/dashboard")


# /////////////////////// Delete account confirmed ///////////////////////
@app.route("/delete_account_confirmed")
def delete_account():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE  userid = %s",
                (session["delete_userid"],))
    mysql.connection.commit()
    cur.close()
    session.pop("account_exists", None)
    session.pop("delete_userid", None)
    return redirect("/")


# /////////////////////// Delete account check ///////////////////////
@app.route("/delete_check", methods=["GET", "POST"])
def delete_check():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT userid,password FROM users WHERE username=%s ",
            (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[1], password):
            session["account_exists"] = True
            session["delete_userid"] = user[0]
            mysql.connection.commit()
            cur.close()
            return render_template("delete_account.html",
                                   account_exists=session["account_exists"])
        else:
            error = True
            cur.close()
            return render_template("delete_account.html", error=error)
    return render_template("delete_account.html")


# /////////////////////// Logout ///////////////////////
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# /////////////////////// Toggle_status ///////////////////////
@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    if "userid" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute("SELECT status FROM tasks WHERE id=%s AND userid=%s",
                (task_id, session["userid"]))
    row = cur.fetchone()

    if row is None:
        cur.close()
        return redirect("/dashboard")

    current = row[0]

    new_status = 0 if current == 1 else 1

    cur.execute("UPDATE tasks SET status=%s WHERE id=%s AND userid=%s",
                (new_status, task_id, session["userid"]))

    mysql.connection.commit()
    cur.close()

    return redirect("/dashboard")


# /////////////////////// Edit_task ///////////////////////
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    if "userid" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()

    if request.method == "POST":
        task_text = request.form["task"]
        deadline = request.form["deadline"]
        priority = request.form["priority"]

        cur.execute("""
            UPDATE tasks SET task_text=%s, deadline=%s, priority=%s
            WHERE id=%s AND userid=%s
        """, (task_text, deadline, priority, task_id, session["userid"]))

        mysql.connection.commit()
        cur.close()
        return redirect("/dashboard")

    cur.execute("SELECT task_text, deadline, priority FROM tasks WHERE id=%s AND userid=%s",
                (task_id,session["userid"]))
    task = cur.fetchone()
    cur.close()

    return render_template("edit.html", task=task, id=task_id)


# /////////////////////// Delete_task ///////////////////////
@app.route("/delete/<int:task_id>")
def delete(task_id):
    if "userid" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s AND userid=%s",
                (task_id, session["userid"]))
    mysql.connection.commit()
    mysql.connection.commit()
    cur.close()

    return redirect("/dashboard")


@app.route("/settings", methods=["GET", "POST"])
def settings():
    """
    Settings route
    """
    if "userid" not in session:
        return redirect("/login")

    userid = session["userid"]

    if request.method == "POST":
        theme = request.form["theme"].strip().lower()
        language = request.form["language"].strip().lower()
        session["lang"] = language
        session["theme"] = theme

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE user_settings
            SET theme = %s, language = %s
            WHERE userid = %s
        """, (theme, language, userid))
        mysql.connection.commit()
        cur.close()
        return redirect("/dashboard")
    return render_template("settings.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """
    Dashboard route
    """
    if "userid" not in session:
        return redirect("/login")

    userid = session["userid"]

    if request.method == "POST":
        task_text = request.form["task"]

        deadline = request.form["deadline"]
        priority = request.form["priority"]

        if deadline == "":
            deadline = None

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO tasks (task_text, deadline, priority, status, userid)
            VALUES (%s, %s, %s, 0, %s)
        """, (task_text, deadline, priority, userid))
        mysql.connection.commit()
        cur.close()

    # Sort
    sort = request.args.get("sort", "priority")

    if sort == "name":
        order_by = "task_text ASC"

    elif sort == "deadline":
        order_by = "deadline ASC"

    else:  # Priority default sorting
        order_by = """
            CASE priority
                WHEN 'urgent' THEN 1
                WHEN 'important' THEN 2
                ELSE 3
            END,
            deadline IS NULL,
            deadline ASC
        """

    cur = mysql.connection.cursor()
    cur.execute(f"""
        SELECT id, task_text, deadline, priority, status
        FROM tasks WHERE userid=%s
        ORDER BY {order_by}
    """, (userid,))
    tasks = cur.fetchall()
    cur.close()
    print(tasks)

    today = datetime.date.today()

    return render_template(
        "dashboard.html",
        tasks=tasks,
        today=today,
        username=session.get("username", "")
    )


if __name__ == "__main__":
    app.run(debug=True)
