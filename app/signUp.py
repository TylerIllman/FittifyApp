from flask import Blueprint, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
import re

load_dotenv()

signup_blueprint = Blueprint("signup", __name__)


@signup_blueprint.route("/signup", methods=["GET"])
def home():
    error_msg = request.args.get("error", "")  # get the 'error' query parameter
    return render_template("signUp.html", error=error_msg)


def validate_email(email):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


@signup_blueprint.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    # Validation
    error_msg = ""
    if not username:
        error_msg = "Username cannot be empty."
    elif not re.match("^[a-zA-Z0-9_]+$", username):  # Match only certain characters
        error_msg = "Username contains invalid characters. Only lowercase and uppercase letters, digits, and underscores are allowed."
    elif not email:
        error_msg = "Email cannot be empty."
    elif not validate_email(email):
        error_msg = "Invalid email format."
    elif not password:
        error_msg = "Password cannot be empty."
    elif len(password) < 8:  # Check if password length is less than 8
        error_msg = "Password should be at least 8 characters long."

    if error_msg:
        # If there's an error, redirect back to sign up page with the error message
        return redirect(url_for("signup.home", error=error_msg))

    hashed_password = generate_password_hash(password)
    print("Form data:", username, email, password)

    # Check if the username or email is already in use
    db_path = os.getenv("DATABASE_URL")
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Convert username and email to lowercase before comparing
        c.execute(
            "SELECT COUNT(*) FROM DimUser WHERE LOWER(Username) = LOWER(?) OR LOWER(Email) = LOWER(?)",
            (username, email),
        )
        result = c.fetchone()

        if result[0] > 0:
            # User already exists, redirect back to sign up page with error message
            error_msg = "Username or email already in use."

            if "UserID" in session:
                session.pop("UserID")  # Remove UserID from session if signup fails

            return redirect(url_for("signup.home", error=error_msg))
        else:
            # Store the form data in the UserDim table
            try:
                c.execute(
                    "INSERT INTO DimUser (Username, PasswordValue, Email) VALUES (?, ?, ?)",
                    (username, hashed_password, email),
                )

                # Get the UserID of the newly created user
                c.execute("SELECT last_insert_rowid()")
                result = c.fetchone()
                user_id = result[0]

                print("Before setting session:", session)  # Add this line
                session["UserID"] = user_id  # Set the UserID in the session
                print("After setting session:", session)  # Add this line

                return redirect(
                    url_for("personalinfo.home")
                )  # Redirect to personal info page
            except sqlite3.Error as e:
                print("Error:", e)
            conn.commit()
            print("Data committed to the database.")
    return redirect(url_for("personalinfo.home"))
