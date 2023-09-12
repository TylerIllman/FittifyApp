from flask import (
    Flask,
    Blueprint,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
    session,
)
from datetime import datetime
import sqlite3
from dotenv import load_dotenv
import os
from app.chatbot import get_db_path
from .fittifyUtils import checkUserDetails

load_dotenv()

app = Flask(__name__)

personalinfo_blueprint = Blueprint("personalinfo", __name__)


@personalinfo_blueprint.route("/personalinfo")
def home():
    auth_check = checkUserDetails(checkDimProfile=False)
    if auth_check:
        return auth_check

    UserID = session["UserID"]
    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT * FROM DimProfile WHERE UserID = ? ORDER BY TimeValue DESC LIMIT 1",
            (UserID,),
        )
        data = c.fetchone()
    # get the error message from the query parameters
    error = request.args.get("error")

    # pass the error to the template
    return render_template("clientpersonaldata.html", data=data, error=error)


@personalinfo_blueprint.route("/process-form", methods=["POST"])
def process_form():
    form_data = request.form
    gender = form_data.get("gender")
    weight = form_data.get("weight")
    height = form_data.get("height")
    fitness_goals = form_data.get("fitness-goals")
    diet = form_data.get("diet")
    workoutdays = form_data.get("workoutdays")
    workoutmins = form_data.get("workoutmins")
    accessgym = form_data.get("accessgym")

    UserID = session["UserID"]

    # Get the current time
    current_time = datetime.now()
    # Open database connection
    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()
        # Store the form data in the DimProfile table
        try:
            c.execute(
                "INSERT INTO DimProfile (UserID, Gender, WeightValue, Height, Goal, Diet, WorkOutDays, WorkOutMin, AccessGym, TimeValue) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    UserID,
                    gender,
                    weight,
                    height,
                    fitness_goals,
                    diet,
                    workoutdays,
                    workoutmins,
                    accessgym,
                    current_time,
                ),
            )
            print(
                "Client data added:",
                UserID,
                gender,
                weight,
                height,
                fitness_goals,
                diet,
                workoutdays,
                workoutmins,
                accessgym,
            )
        except sqlite3.Error as e:
            print("Error:", e)
        conn.commit()
        print("Data committed to the database.")

    return redirect(url_for("chatbot.chatbot"))


@personalinfo_blueprint.route("/show-dim-profile")
def show_dim_profile():
    # Open database connection
    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()
        # Get all data from the DimProfile table
        c.execute("SELECT * FROM FactConversation")
        data = c.fetchall()
    # Convert the data to a string
    str_data = "\n".join(map(str, data))
    # Return the string
    return str_data


if __name__ == "__main__":
    app.run
