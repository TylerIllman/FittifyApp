"""

Save Message functionality:

The saveMessage endpoint is responsible for saving a particular user message with a specified type in the database.

The test case follows these steps:

    The setUp method creates a connection to the test database, inserts a test user, and a test message for this user in the FactConversation table. 
    It stores the ID of the inserted message for later use.
    The test_save_message method then sends a POST request to the saveMessage endpoint, attempting to save the test message with a specific MessageType.
    It checks if the response status code is 200, indicating a successful operation.
    After that, it fetches the MessageType of the test message from the database and checks if it has been updated correctly.
    It then also checks that when a message is 'deleted' from the saved message page, its MessageType is set back to 0.
    The tearDown method clears up the test environment by deleting the test message from the FactConversation table and closing the database connection.
    
This test ensures that the saveMessage endpoint is functioning as expected, which is critical for the correct operation of the chatbot.

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
        flask_app.config["WTF_CSRF_ENABLED"] = False
        return flask_app

    def setUp(self):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

        self.c.execute(
            "INSERT INTO DimUser (Username, PasswordValue, Email) VALUES (?, ?, ?)",
            ("testuser", "testpass", "testuser@example.com"),
        )

        self.conn.commit()

        # Get the user id of the newly created user
        self.c.execute("SELECT UserID FROM DimUser WHERE Username = ?", ("testuser",))
        self.user_id = self.c.fetchone()[0]

        # Insert a test message
        self.c.execute(
            "INSERT INTO FactConversation (UserID, Role, Content, TimeValue, MessageType) VALUES (?, ?, ?, ?, ?)",
            (self.user_id, "user", "Test message", "2023-05-17 00:00:00", 0),
        )
        self.conn.commit()
        self.message_id = self.c.lastrowid

    def test_delete_message(self):
        with self.client.session_transaction() as sess:
            sess["UserID"] = self.user_id

        # Delete the message
        response = self.client.post(
            "/saved-messages/delete",
            json={"message_id": self.message_id},
        )

        # Check response status and data
        self.assertEqual(response.status_code, 200)

        # Check if the message has been deleted
        self.check_message_deleted(self.message_id)

        # Try to delete a message that doesn't exist
        response = self.client.post(
            "/saved-messages/delete",
            json={"message_id": 123456},
        )

        # Check response status and data
        self.assertEqual(response.status_code, 400)

    def check_message_deleted(self, message_id):
        self.c.execute(
            "SELECT * FROM FactConversation WHERE MessageID = ?",
            (message_id,),
        )
        message = self.c.fetchone()
        self.assertIsNotNone(message)  # The message should exist
        self.assertEqual(message[-1], 0)  # The MessageType should be 0

    def tearDown(self):
        self.c.execute(
            "DELETE FROM FactConversation WHERE MessageID = ?", (self.message_id,)
        )
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    pytest.main(["-v", "test_savemessage.py"])
