import sqlite3
from flask import render_template, session, redirect, url_for
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def get_db_path():
    # Retrieves the path to the SQLite database file based on the DATABASE_URL environment variable
    script_dir = Path(__file__).resolve().parent.parent
    db_filename = os.getenv("DATABASE_URL")
    return script_dir / db_filename


def logoutUser():
    # Clears the session, effectively logging out the user
    session.clear()


def checkUserDetails(checkDimProfile=True):
    print("authenticating user")

    if "UserID" not in session:
        # If UserID is not present in the session, redirect the user to the login page
        print("UserID not in session")
        return redirect(url_for("login.loginPage"))

    UserID = session["UserID"]
    print("UserID: ", UserID)

    if checkDimProfile:
        with sqlite3.connect(get_db_path()) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM DimProfile WHERE UserID = ?", (UserID,))
            rows = c.fetchall()
            print("these are the rows: ", rows)
            if len(rows) == 0:
                # If no rows are found for the user in the DimProfile table, redirect to the profile setup page
                return redirect(
                    url_for(
                        "personalinfo.home",
                        error="Please finish setting up your profile",
                    )
                )


def genSystemPrompt(dimProfileRow):
    # Generates a system prompt based on the user's profile data
    print("THIS IS THE DIM PROFILE ROW:", dimProfileRow)

    gender = dimProfileRow[0]
    weightValue = dimProfileRow[1]
    height = dimProfileRow[2]
    goal = dimProfileRow[3]
    diet = dimProfileRow[4]
    workoutDays = dimProfileRow[5]
    workoutMins = dimProfileRow[6]
    accessToGym = dimProfileRow[7]

    systemPrompt = {
        "role": "system",
        "content": f"You're Fittify, an AI fitness coach. User Info: Gender {gender}, weight (kg): {weightValue}, height (cm): {height}, goal: {goal}, Diet: {diet}, workout {workoutDays} days for {workoutMins} mins, {accessToGym} gym access. Be polite, fun, and encouraging. Provide fitness advice ONLY.",
    }

    return systemPrompt
