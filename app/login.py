import sqlite3
from flask import render_template, request, redirect, url_for, session, Blueprint, flash
from dotenv import load_dotenv
from werkzeug.security import check_password_hash
import os
from pathlib import Path

load_dotenv()

login_blueprint = Blueprint("login", __name__)


def get_db_path():
    script_dir = Path(__file__).resolve().parent.parent
    db_filename = os.getenv("DATABASE_URL")
    return script_dir / db_filename


@login_blueprint.route("/login", methods=["GET"])
def loginPage():
    if "UserID" in session:
        return redirect(url_for("chatbot.chatbot"))
    return render_template("login.html")


@login_blueprint.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    print("Form data:", username, password)

    print(f"Database path: {get_db_path()}")
    #with sqlite3.connect(get_db_path()) as conn:

    # Connect to the SQLite database
    with sqlite3.connect(str(get_db_path())) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        # Retrieve the user information from the database based on the provided username
        c.execute(
            "SELECT * FROM DimUser WHERE Username = ?",
            (username,),
        )
        user = c.fetchone()

        # Check if the user exists and if the password is correct
        if user is None or not check_password_hash(user["PasswordValue"], password):
            flash("Username or password is incorrect.")
            return redirect(url_for("login.loginPage"))
        else:
            session.permanent = True  # Set the session as permanent
            session["UserID"] = user["UserID"]
            return redirect(url_for("chatbot.chatbot"))
