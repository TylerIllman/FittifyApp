"""

Chat functionality:

    Database Integration: It checks if the application can successfully interact with the SQLite database. 
    It does this by inserting test data into the DimUser and DimProfile tables, deleting data, and fetching data.

    User Session Management: The test checks if the application can set and retrieve session data (specifically the UserID).

    Chatbot API Functionality: The test sends a POST request to the /chatbot/api endpoint with test data to simulate a user 
    sending a message to the chatbot. It checks if the chatbot can correctly receive and handle this request.

    Chatbot Response: It verifies that the chatbot responds correctly to a user message. It checks the response for the appropriate 
    keys and values, ensuring that the role is "assistant" and the content key exists.

    Chat History Storage: The test checks if the chat history is correctly stored in the FactConversation table in the database. 
    It verifies that there is at least one chat message associated with the test user.

    Cleanup: Finally, the test ensures that the test data inserted into the database is removed after the test is run. 
    
"""


import pytest
import sqlite3
from flask import session
from app.main import app
from app.chatbot import chatbot_blueprint
from app.main import app
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

app.config["TESTING"] = True


db_path = os.path.join(os.getcwd(), "tests", "test_db.db")
os.environ["DATABASE_URL"] = db_path
print(os.path.exists(db_path))

print(f'DATABASE_URL: {os.getenv("DATABASE_URL")}')
print(f"db_path: {db_path}")


# Establish an application context before running the tests.
@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            yield client


def test_chat(client):
    # Connect to the database and insert a test user
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()

        cur.execute("DELETE FROM FactConversation")
        cur.execute("DELETE FROM DimUser")
        cur.execute("DELETE FROM DimProfile")
        conn.commit()

        cur.execute(
            "INSERT INTO DimUser (Username, PasswordValue, Email) VALUES (?, ?, ?)",
            ("test_user", "test_user", "test_user@test.test"),
        )

        conn.commit()

        cur.execute("SELECT * FROM DimProfile")
        testRow = cur.fetchall()
        print(testRow)

        # Get the UserID of the newly inserted test user
        cur.execute("SELECT UserID FROM DimUser WHERE Username = ?", ("test_user",))
        test_user_id = cur.fetchone()[0]
        print(test_user_id)

        cur.execute(
            "INSERT INTO DimProfile (UserID, Gender, WeightValue, Height, Goal, Diet, WorkOutDays, WorkOutMin, AccessGym, TimeValue) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                test_user_id,
                "male",
                50,
                50,
                "endurance",
                "vegan",
                4,
                45,
                "yes",
                datetime.now(),
            ),
        )

        cur.execute("SELECT * FROM DimProfile")
        testRow = cur.fetchall()
        print(testRow)

    # Assuming '/login' route sets the 'UserID' in session
    with client.session_transaction() as session:
        session["UserID"] = test_user_id
        print(session["UserID"])

        cur.execute(
            "SELECT Gender, WeightValue, Height, Goal, Diet, WorkOutDays, WorkOutMin, AccessGym FROM DimProfile WHERE UserID = ? ORDER BY TimeValue ASC LIMIT 1",
            (session["UserID"],),
        )
        userDetails = cur.fetchall()
        print(userDetails)

    # Send a message to the chatbot
    rv = client.post("/chatbot/api", json={"content": "test message", "role": "user"})

    # Check if the user receives a message back
    response_data = rv.get_json()
    assert "role" in response_data and response_data["role"] == "assistant"
    assert "content" in response_data

    # Check if the chat is stored in the database
    cur.execute(
        "SELECT * FROM FactConversation WHERE UserID = ? ORDER BY TimeValue ASC",
        (test_user_id,),
    )
    rows = cur.fetchall()

    # Check if there's any chat from the test_user
    assert len(rows) > 0

    # Check if the first message from the assistant is a system prompt
    # assert rows[0][2] == "system"

    cur.execute("DELETE FROM FactConversation WHERE UserID = ?", (test_user_id,))
    cur.execute("DELETE FROM DimUser WHERE UserID = ?", (test_user_id,))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    pytest.main(["-v", "test_chat.py"])
