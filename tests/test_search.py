"""

Search functionality:

setUp: This method sets up the testing environment before each test. It creates a new user in the database to simulate a user session.

test_search: This method is the actual test case. It tests the search() function by first simulating a user sending a few messages through the chatbot.
Then, it simulates a search request, checking if the function correctly identifies and returns the IDs of the messages that contain the search term. 
The test validates the status code of the response, the number of returned results, and the actual IDs of the messages.

tearDown: This method is run after each test to clean up the testing environment. It deletes the user created during setup from the database.
The test module ends with a command that runs the tests when the module is executed directly.
This module helps ensure the integrity of the search functionality of our chatbot, 
making sure it accurately retrieves messages based on user search terms.

"""

import pytest
from flask import session, url_for, json
from flask_testing import TestCase
from app.main import app as flask_app
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.path.join(os.getcwd(), "tests", "test_db.db")
os.environ["DATABASE_URL"] = db_path
print(os.path.exists(db_path))


class TestSearch(TestCase):
    def create_app(self):
        flask_app.config["TESTING"] = True
        return flask_app

    def setUp(self):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO DimUser (Username, PasswordValue, Email) VALUES (?, ?, ?)",
                ("testuser", "testpass", "testuser@example.com"),
            )
            conn.commit()

            # Get the user id of the newly created user
            c.execute("SELECT UserID FROM DimUser WHERE Username = ?", ("testuser",))
            user_id = c.fetchone()[0]

            # Insert some messages for the test user
            c.execute(
                "INSERT INTO FactConversation (UserID, Role, Content, TimeValue, MessageType) VALUES (?, ?, ?, datetime('now'), ?)",
                (user_id, "user", "This is a test message", 0),
            )
            c.execute(
                "INSERT INTO FactConversation (UserID, Role, Content, TimeValue, MessageType) VALUES (?, ?, ?, datetime('now'), ?)",
                (user_id, "user", "This is another test message", 0),
            )
            conn.commit()

            # Set the user id in the session so the search function can use it
            with self.client.session_transaction() as sess:
                sess["UserID"] = user_id

    def get_message_content_by_id(self, message_id):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT Content FROM FactConversation WHERE MessageID = ?",
                (message_id,),
            )
            content = c.fetchone()[0]
        return content

    def test_search(self):
        response = self.client.post(
            url_for("chatbot.search"), json={"searchTerm": "test"}
        )
        data = json.loads(response.data)

        assert response.status_code == 200
        assert len(data["searchResult"]) == 2

        contents = [self.get_message_content_by_id(id) for id in data["searchResult"]]
        assert "This is a test message" in contents
        assert "This is another test message" in contents

    def test_search_no_results(self):
        response = self.client.post(
            url_for("chatbot.search"), json={"searchTerm": "no match"}
        )
        data = json.loads(response.data)

        assert response.status_code == 200
        assert len(data["searchResult"]) == 0

    def test_search_case_insensitive(self):
        response = self.client.post(
            url_for("chatbot.search"), json={"searchTerm": "TEST"}
        )
        data = json.loads(response.data)

        assert response.status_code == 200
        assert len(data["searchResult"]) == 2

        contents = [self.get_message_content_by_id(id) for id in data["searchResult"]]
        assert "This is a test message" in contents
        assert "This is another test message" in contents

    def tearDown(self):
        with sqlite3.connect(db_path) as conn:
            c = conn.cursor()
            c.execute(
                "DELETE FROM DimUser WHERE Username = ?",
                ("testuser",),
            )
            c.execute(
                "DELETE FROM FactConversation WHERE Content LIKE ?",
                ("%test%",),
            )
            conn.commit()


if __name__ == "__main__":
    pytest.main(["-v", "test_chat.py"])
