from flask import (
    Blueprint,
    jsonify,
    request,
    render_template,
    session,
    url_for,
    redirect,
)
from flask_socketio import join_room, leave_room, send
import openai       
import sqlite3
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import os
from .fittifyUtils import checkUserDetails, genSystemPrompt

load_dotenv()

chatbot_blueprint = Blueprint("chatbot", __name__)

# # Define the system prompt for the chatbot
# systemPrompt = {
#     "role": "system",
#     "content": "You are FitBot, an AI personal trainer. Your purpose is to assist exclusively with fitness-related queries. Be polite, fun, and encouraging. Make sure your responses are short, focused, and relevant to fitness. When asked for workout or meal plans, request specifics like weight, goal, frequency, how many days a week, and duration of daily workouts. Should a non-fitness related question arise, politely inform the user that you are only equipped to provide fitness-related guidance. Ensure your responses are formatted for readability.",
# }


def get_db_path():
    script_dir = Path(__file__).resolve().parent.parent
    db_filename = os.getenv("DATABASE_URL")
    return script_dir / db_filename


@chatbot_blueprint.route("/chatbot", methods=["GET"])
def chatbot():
    # Check if the user is authenticated
    auth_check = checkUserDetails()
    if auth_check:
        return auth_check

    UserID = session["UserID"]

    # Retrieve the chat history for the user from the database
    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()
        try:
            c.execute(
                "SELECT Role, Content, MessageID, TimeValue FROM FactConversation WHERE UserID = ?",
                (UserID,),
            )
        except sqlite3.Error as e:
            print("Error:", e)
        chatHistory = c.fetchall()

    return render_template("chatbot.html", chatHistory=chatHistory)


@chatbot_blueprint.route("/chatbot/api", methods=["POST", "GET"])
def chat():
    # Get the request data as JSON
    data = request.get_json()
    if "content" not in data:
        return jsonify({"error": "Invalid request"}), 400

    print("printing data: ", data)

    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO FactConversation (UserID, Role, Content, TimeValue, MessageType) VALUES (?, ?, ?, ?, ?)",
                (
                    session["UserID"],
                    data["role"],
                    data["content"],
                    datetime.now(),
                    0,
                ),
            )

            # Get the ID of the user message
            userMessageID = c.lastrowid  

            # Retrieve the chat history for the user from the database
            c.execute(
                "SELECT Role, Content FROM FactConversation WHERE UserID = ? ORDER BY TimeValue DESC LIMIT 10",
                (session["UserID"],),
            )
            chatHistory = c.fetchall()

            # Retrieve the user details from the database
            c.execute(
                "SELECT Gender, WeightValue, Height, Goal, Diet, WorkOutDays, WorkOutMin, AccessGym FROM DimProfile WHERE UserID = ? ORDER BY TimeValue DESC LIMIT 1",
                (session["UserID"],),
            )
            userDetails = c.fetchall()

        except sqlite3.Error as e:
            print("Error:", e)
        conn.commit()
        print("Data committed to the database.")

        # Convert chat history to a pandas DataFrame
        chatHistory_df = pd.DataFrame(chatHistory, columns=["role", "content"])
        chatHistory_dicts = chatHistory_df.to_dict("records")
        chatHistory_dicts.reverse()
        print(userDetails)
        systemPrompt = genSystemPrompt(userDetails[0])

        # Add the system prompt to the chat history
        chatHistory_dicts.insert(0, systemPrompt)

        print("CHAT HISTORY DICTS: ", chatHistory_dicts)

    try:
        openai.api_key = "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"

        # Generate an AI response using OpenAI Chat API
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chatHistory_dicts,
        )

        assistantResponseContent = completion.choices[0].message["content"]

        with sqlite3.connect(get_db_path()) as conn:
            c = conn.cursor()
            try:
                # Insert the assistant response into the database
                c.execute(
                    "INSERT INTO FactConversation (UserID, Role, Content, TimeValue, MessageType) VALUES (?, ?, ?, ?, ?)",
                    (
                        session["UserID"],
                        "assistant",
                        assistantResponseContent,
                        datetime.now(),
                        0,
                    ),
                )
                assistantMessageID = (
                    c.lastrowid
                )  # Get the ID of the message just inserted

            except sqlite3.Error as e:
                print("Error:", e)
            conn.commit()

        response = {
            "role": "assistant",
            "content": assistantResponseContent,
            "userMessageID": userMessageID,
            "assistantMessageID": assistantMessageID,
        }

        print("Data committed to the database.")

        return response, 200
    except Exception as e:
        print("in except: ", e)
        return jsonify({"error": str(e)}), 500


@chatbot_blueprint.route("/chatbot/api/search", methods=["POST"])
def search():
    data = request.get_json()

    if "searchTerm" not in data:
        return jsonify({"error": "Invalid request"}), 400

    searchTerm = data["searchTerm"].lower()

    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()
        try:
            # Retrieve all messages for the user from the database
            c.execute(
                "SELECT MessageID, Content FROM FactConversation WHERE UserID = ?",
                (session["UserID"],),
            )
        except sqlite3.Error as e:
            print("Error:", e)
        searchResults = c.fetchall()

    # Filter the search results based on the search term
    messageIdList = [
        entry[0] for entry in searchResults if searchTerm in entry[1].lower()
    ]
    print("messageIdList: ", messageIdList)

    return jsonify({"searchResult": messageIdList}), 200


@chatbot_blueprint.route("/chatbot/api/savemessage", methods=["POST"])
def saveMessage():
    data = request.get_json()

    # ADD CHECK FOR MessageSaveType
    if "messageID" not in data:
        return jsonify({"error": "Invalid request"}), 400

    messageId = data["messageID"]
    messageSaveType = data["messageSaveType"]

    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT 1 FROM FactConversation WHERE MessageID = ?",
            (messageId,),
        )
        if c.fetchone() is None:
            return jsonify({"error": "Message does not exist"}), 400
        try:
            # Update the message type in the database
            c.execute(
                "UPDATE FactConversation SET MessageType = ? WHERE MessageID = ?",
                (messageSaveType, messageId),
            )
        except sqlite3.Error as e:
            print("Error:", e)
        conn.commit()

    return jsonify({"content": "Message Saved"}), 200


@chatbot_blueprint.route("/chatbot/api/logout", methods=["GET"])
def logoutUser():
    print("in logout")
    session.clear()
    return redirect(url_for("login.loginPage"))


@chatbot_blueprint.route("/home")
def home():
    return render_template("landingPage.html")
