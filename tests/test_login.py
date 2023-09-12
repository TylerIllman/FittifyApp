"""
Login functionality:
It verifies the following scenarios:

1. Successful login for a registered user, ensuring the correct redirection and session management.
2. Successful login for a returning user, verifying the correct redirection to the chat page.
3. Failed login attempt with incorrect username or password, checking for the appropriate error message and session behavior.
4. Login request with null values for username and password, validating the handling of a bad request.

"""

import pytest
import sqlite3
from flask import session
from app.main import app
from app.login import login_blueprint
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash

load_dotenv()

app.config["TESTING"] = True

UserID = None


def setup_module(module):
    global UserID
    db_path = os.path.join(os.getcwd(), "tests", "test_db.db")
    os.environ["DATABASE_URL"] = db_path
    print(os.path.exists(db_path))

    hashed_password_testuser = generate_password_hash("testpass")
    hashed_password_returninguser = generate_password_hash("returningpass")

    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO DimUser (Username, PasswordValue, Email) VALUES (?, ?, ?)",
            ("testuser", hashed_password_testuser, "testuser@example.com"),
        )
        conn.commit()

    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO DimUser (Username, PasswordValue, Email) VALUES (?, ?, ?)",
            (
                "returninguser",
                hashed_password_returninguser,
                "returninguser@example.com",
            ),
        )
        UserID = c.lastrowid  # Get the id of the user just inserted
        c.execute(
            "INSERT INTO DimProfile (UserID, Gender, WeightValue, Height, Goal, Diet, WorkOutDays, WorkOutMin, AccessGym, TimeValue) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))",
            (
                UserID,
                "male",
                50,
                50,
                "endurance",
                "vegan",
                4,
                45,
                "yes",
            ),  # Add a profile for the returning user
        )
        conn.commit()
        c.execute("SELECT * FROM DimUser")
        testRow = c.fetchall()
        print(testRow)
        c.execute("SELECT * FROM DimProfile")
        testRow = c.fetchall()
        print(testRow)


def test_login_success():
    test_app = app.test_client()
    response = test_app.post(
        "/login",
        data={"username": "testuser", "password": "testpass"},
        follow_redirects=True,
    )
    print(response.data)
    assert (
        response.status_code == 200
    )  # 200 status code means request has succeeded and you're at the redirected page
    assert (
        b'<form action="/process-form"' in response.data
    )  # Check the redirected page contains "chatbot" indicating it's the correct page
    with test_app.session_transaction() as sess:
        assert sess["UserID"] is not None  # check if UserID has been set in session
        assert sess["_permanent"] is True  # check if permanent session is set


def test_login_success_returning_user():
    test_app = app.test_client()
    response = test_app.post(
        "/login",
        data={"username": "returninguser", "password": "returningpass"},
        follow_redirects=True,
    )
    print(response.data)
    assert (
        response.status_code == 200
    )  # 200 status code means request has succeeded and you're at the redirected page
    assert (
        b"<title>Chat Page</title>" in response.data
    )  # Check the redirected page contains "chatbot" indicating it's the correct page


def test_login_fail():
    test_app = app.test_client()
    response = test_app.post(
        "/login",
        data={"username": "wronguser", "password": "wrongpass"},
        follow_redirects=True,
    )
    print(response.data)
    assert (
        response.status_code == 200
    )  # 200 status code means request has succeeded and you're at the login page
    assert (
        b"Username or password is incorrect." in response.data
    )  # Check if the error message is displayed in response data
    with test_app.session_transaction() as sess:
        assert "UserID" not in sess  # check if UserID has not been set in session


def test_login_null():
    test_app = app.test_client()
    response = test_app.post(
        "/login", data={"username": None, "password": None}, follow_redirects=True
    )
    print(response.data)
    assert (
        response.status_code == 400
    )  # 400 status code means bad request, as we're sending None for username and password


def teardown_module(module):
    global UserID
    db_path = os.path.join(os.getcwd(), "tests", "test_db.db")
    os.environ["DATABASE_URL"] = db_path
    print(os.path.exists(db_path))
    with sqlite3.connect(db_path) as conn:
        # with sqlite3.connect("tests/test_db.db") as conn:
        c = conn.cursor()
        c.execute(
            "DELETE FROM DimUser WHERE Username = ? OR Username = ?",
            ("testuser", "returninguser"),
        )
        c.execute(
            "DELETE FROM DimProfile WHERE UserID = ?",
            (UserID,),
        )
        conn.commit()


if __name__ == "__main__":
    pytest.main(["-v", "test_login.py"])
