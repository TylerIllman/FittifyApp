"""

Signup functionality:

The tests simulate different scenarios to verify the behavior of the signup process. 
The tests cover successful signup, empty username, empty password, duplicate usernames 
(case sensitive and case insensitive), disallowed characters in the username, and duplicate email addresses. 

"""

import pytest
import sqlite3
from flask import session
from app.main import app
from app.signUp import signup_blueprint
from dotenv import load_dotenv
import os
from werkzeug.urls import url_parse

load_dotenv()

app.config["TESTING"] = True
app.config[
    "WTF_CSRF_ENABLED"
] = False  # If you have CSRF protection enabled, disable it for testing


@pytest.fixture(autouse=True)
def reset_db():
    db_path = os.path.join(os.getcwd(), "tests", "test_db.db")
    os.environ["DATABASE_URL"] = db_path
    print(os.path.exists(db_path))
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM DimUser")
    conn.commit()
    yield conn  # yield the connection instead of closing it
    conn.close()  # close the connection after the test is done


@pytest.fixture
def insert_test_user():
    db_path = os.path.join(os.getcwd(), "tests", "test_db.db")
    with sqlite3.connect(db_path) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO DimUser (Username, PasswordValue, Email) VALUES (?, ?, ?)",
            ("testuser", "testpass", "testuser@example.com"),
        )
        conn.commit()


def test_signup_success():
    with app.test_client() as test_app:
        response = test_app.post(
            "/signup",
            data={
                "username": "testuser2",
                "email": "testuser2@example.com",
                "password": "testpass2",
            },
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        )
        assert response.status_code == 302
        assert url_parse(response.location).path == "/personalinfo"


def test_signup_empty_username():
    with app.test_client() as test_app:
        response = test_app.post(
            "/signup",
            data={
                "username": "",
                "email": "testuser@example.com",
                "password": "testpass",
            },
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        )
        assert response.status_code == 302
        assert url_parse(response.location).path == "/signup"


def test_signup_empty_password():
    with app.test_client() as test_app:
        response = test_app.post(
            "/signup",
            data={
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "",
            },
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        )
        assert response.status_code == 302
        assert url_parse(response.location).path == "/signup"


def test_signup_duplicate_username(insert_test_user):
    with app.test_client() as test_app:
        response = test_app.post(
            "/signup",
            data={
                "username": "testuser",
                "email": "differentuser@example.com",
                "password": "testpass",
            },
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        )
        assert response.status_code == 302
        assert url_parse(response.location).path == "/signup"


def test_signup_duplicate_username_case_insensitive(insert_test_user):
    with app.test_client() as test_app:
        response = test_app.post(
            "/signup",
            data={
                "username": "TESTUSER",  # Same username as insert_test_user, but in uppercase
                "email": "differentuser@example.com",
                "password": "testpass",
            },
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        )
        assert response.status_code == 302
        assert url_parse(response.location).path == "/signup"


def test_signup_username_disallowed_characters():
    with app.test_client() as test_app:
        response = test_app.post(
            "/signup",
            data={
                "username": "test/user",  # Disallowed character (/) in username
                "email": "testuser@example.com",
                "password": "testpass",
            },
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        )
        assert response.status_code == 302
        assert url_parse(response.location).path == "/signup"


def test_signup_username_disallowed_characters():
    with app.test_client() as test_app:
        response = test_app.post(
            "/signup",
            data={
                "username": "test/user",  # Disallowed character (/) in username
                "email": "testuser@example.com",
                "password": "testpass",
            },
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        )
        assert response.status_code == 302
        assert url_parse(response.location).path == "/signup"


def test_signup_duplicate_email(insert_test_user):
    with app.test_client() as test_app:
        response = test_app.post(
            "/signup",
            data={
                "username": "differentuser",
                "email": "testuser@example.com",
                "password": "testpass",
            },
            environ_base={"REMOTE_ADDR": "127.0.0.1"},
        )
        assert response.status_code == 302
        assert url_parse(response.location).path == "/signup"


if __name__ == "__main__":
    pytest.main(["-v", "test_signup.py"])
