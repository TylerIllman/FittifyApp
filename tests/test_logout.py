"""
Logout functionality: 

    The test cases include testing logout with a logged-in user and testing logout without a previous login. 
    The user's session is cleared upon logout, verified by checking that UserID is not in the session after the logout operation.
    A successful redirect occurs after the logout, indicated by a 302 status code.
    The redirect location is the login page. This is checked by asserting that the response's location URL ends with the URL for the login page.
    
"""

import pytest
from flask import session, url_for
from flask_testing import TestCase
from app.main import app as flask_app
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.path.join(os.getcwd(), "tests", "test_db.db")
os.environ["DATABASE_URL"] = db_path
print(os.path.exists(db_path))


class TestLogout(TestCase):
    def create_app(self):
        flask_app.config["TESTING"] = True
        return flask_app

    def setUp(self):
        self.create_test_user()

    def create_test_user(self):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO DimUser (Username, PasswordValue, Email) VALUES (?, ?, ?)",
                ("testuser", "testpass", "testuser@example.com"),
            )
            conn.commit()

    def delete_test_user(self):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute(
                "DELETE FROM DimUser WHERE Username = ?",
                ("testuser",),
            )
            conn.commit()

    def test_logout(self):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT UserID FROM DimUser WHERE Username = ?",
                ("testuser",),
            )
            test_user_id = c.fetchone()[0]
            print(test_user_id)
        with self.client.session_transaction() as sess:
            sess["UserID"] = test_user_id
            assert sess["UserID"] == test_user_id

        response = self.client.get(url_for("chatbot.logoutUser"))

        with self.client.session_transaction() as sess:
            assert sess.get("UserID") is None

        assert response.status_code == 302
        assert response.location.endswith(url_for("login.loginPage"))

    def test_logout_without_login(self):
        response = self.client.get(url_for("chatbot.logoutUser"))

        with self.client.session_transaction() as sess:
            assert sess.get("UserID") is None

        assert response.status_code == 302
        assert response.location.endswith(url_for("login.loginPage"))

    def tearDown(self):
        self.delete_test_user()


if __name__ == "__main__":
    pytest.main(["-v", "test_chat.py"])
