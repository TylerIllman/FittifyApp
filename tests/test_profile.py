"""

Save Profile functionality:

This file contains a test case for the "Save Profile" functionality of a chatbot app. 
The test case verifies the behavior of saving a user's profile by simulating the form submission process. 
The test sets up a test user in the DimUser table and logs in the user. 
It then submits a form with profile data and checks if the data is properly inserted into the DimProfile table. 
The test confirms that the HTTP response status code is a redirect (302) and asserts the profile details against the submitted form data. 
Finally, the test cleans up by deleting the test user's profiles and the test user from the database. 

"""

import pytest
from flask import session, url_for, json
from flask_testing import TestCase
from app.main import app as flask_app
import sqlite3
import os
from werkzeug.security import generate_password_hash
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

        self.c.execute("DELETE FROM DimUser")
        self.conn.commit()

        # Create a user in DimUser
        hashed_password = generate_password_hash("testpassword")
        print("Hashed password in test setup:", hashed_password)
        self.c.execute(
            "INSERT INTO DimUser (Username, PasswordValue, Email) VALUES (?, ?, ?)",
            ("testuser", hashed_password, "testuser@test.test"),
        )
        self.user_id = self.c.lastrowid  # Get the ID of the newly inserted user
        print(self.user_id)
        self.conn.commit()

        # Assuming a login endpoint where you post username and password.
        self.client.post(
            "/login", data={"username": "testuser", "password": "testpassword"}
        )

    def test_process_form(self):
        with self.client.session_transaction() as sess:
            print(sess)
            user_id = sess["UserID"]

        form_data = {
            "gender": "male",
            "weight": "70",
            "height": "180",
            "fitness-goals": "lose weight",
            "diet": "vegan",
            "activity": "high",
            "workoutdays": "5",
            "workoutmins": "30",
            "accessgym": "yes",
        }

        response = self.client.post("/process-form", data=form_data)
        print(response.data)  # Add this line
        self.assertEqual(response.status_code, 302)  # Since the route redirects

        # Check if the profile was properly inserted
        self.c.execute(
            "SELECT * FROM DimProfile WHERE UserID = ? ORDER BY UserID DESC LIMIT 1",
            (user_id,),
        )
        profile = self.c.fetchone()

        # Assert the profile is not None and its details match the form data
        self.assertIsNotNone(profile)
        self.assertEqual(profile[2], form_data["gender"])
        self.assertEqual(profile[3], int(form_data["weight"]))
        self.assertEqual(profile[4], int(form_data["height"]))
        self.assertEqual(profile[5], form_data["fitness-goals"])
        self.assertEqual(profile[6], form_data["diet"])
        self.assertEqual(profile[7], int(form_data["workoutdays"]))
        self.assertEqual(profile[8], int(form_data["workoutmins"]))
        self.assertEqual(profile[9], form_data["accessgym"])

    def tearDown(self):
        # Delete the test user's profiles and the test user
        self.c.execute("DELETE FROM DimProfile WHERE UserID = ?", (self.user_id,))
        self.c.execute("DELETE FROM DimUser WHERE UserID = ?", (self.user_id,))
        self.conn.commit()
        self.conn.close()
