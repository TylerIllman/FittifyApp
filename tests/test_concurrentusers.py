"""
Concurrent users:

This test uses pytest as the testing framework and the ThreadPoolExecutor from the concurrent.futures module to create a pool of threads. 
Each thread represents a user interacting with the app. 
This test demonstrates functionality for a maximum of 3 users (for more users, increasing the requests from the openAI API is required).
The test case verifies that each user can successfully send a message to the chatbot and receive a response. 
The test utilizes a test client to simulate the interactions and sets the user ID in the session for authentication. 
The test also adds a user profile for each user before sending the message so that it can access UserID for the system prompt. 
The interactions are performed concurrently using multiple threads. 
The test ensures that all threads complete successfully without exceptions. 
The test is run using the pytest command line interface.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from flask.testing import FlaskClient
import pytest
from app.main import app
import sqlite3
from app.chatbot import get_db_path
import time

max_retries = 5
delay = 5  # delay in seconds

# This is to ensure the app is in test mode
app.config["TESTING"] = True
app.test_client_class = FlaskClient


def add_user_profile(user_id):
    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO DimProfile (UserID, Gender, WeightValue, Height, Goal, Diet, WorkOutDays, WorkOutMin, AccessGym, TimeValue) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    user_id,
                    "Male",
                    70,
                    175,
                    "Fitness",
                    "Vegan",
                    5,
                    60,
                    "Yes",
                    "2023-05-17 00:00:00",
                ),
            )
        except sqlite3.Error as e:
            print("Error:", e)
        conn.commit()


def chat_interaction(user_id):
    add_user_profile(user_id)
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess["UserID"] = user_id
        for i in range(max_retries):
            try:
                time.sleep(1)  # Introduce a delay before making the request
                response = client.post(
                    "/chatbot/api",
                    json={
                        "content": f"Test message from user {user_id}",
                        "role": "user",
                    },
                )
                if response.status_code == 200:
                    data = response.get_json()
                    assert "role" in data and data["role"] == "assistant"
                    assert "content" in data
            except Exception:
                if i < max_retries - 1:  # If it's not the final attempt
                    time.sleep(delay)  # Wait for some time before retrying
                    continue  # Go to the next iteration of the loop, i.e., retry the API request
                else:
                    raise  # If it's the final attempt, raise the exception.


def test_concurrent_users():
    # Create a ThreadPoolExecutor. The number passed to the constructor is the number of threads that will be created.
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Use the executor to start 10 threads, each running the chat_interaction function
        futures = {executor.submit(chat_interaction, user_id) for user_id in range(10)}

        # Ensure all threads complete successfully
        for future in as_completed(futures):
            # This will raise an exception if the chat_interaction function threw an exception
            future.result()


if __name__ == "__main__":
    pytest.main(["-v", "test_concurrentusers.py"])
