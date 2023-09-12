from flask import (
    Blueprint,
    render_template,
    session,
    request,
    jsonify,
    url_for,
    redirect,
)
import sqlite3
from dotenv import load_dotenv
import os
from .fittifyUtils import checkUserDetails
from app.chatbot import get_db_path

load_dotenv()

saved_messages_blueprint = Blueprint("savedMessages", __name__)

@saved_messages_blueprint.route("/saved-messages", methods=["GET"])
def saved_messages():
    auth_check = checkUserDetails()
    if auth_check:
        return auth_check
    return render_template("savedMessages.html")

@saved_messages_blueprint.route("/saved-messages/api", methods=["GET"])
def get_saved_messages():
    option = request.args.get("option")
    if "UserID" not in session:
        return redirect(url_for("login.loginPage"))

    UserID = session["UserID"]

    print("UserID: ", UserID)
    # Fetch saved messages based on the selected option and user ID
    # Replace 'YOUR_USER_ID' with the actual user ID

    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()
        try:
            c.execute(
                "SELECT MessageID, Content, strftime('%d/%m/%Y', TimeValue) FROM FactConversation WHERE UserID = ? AND MessageType = ?",
                (UserID, option),
            )
        except sqlite3.Error as e:
            print("Error:", e)
    messages = c.fetchall()
    print(messages)
    conn.close()

    return jsonify({"messages": messages})

@saved_messages_blueprint.route("/saved-messages/delete", methods=["POST"])
def delete_saved_message():
    if "UserID" not in session:
        return redirect(url_for("login.loginPage"))

    UserID = session["UserID"]
    data = request.get_json()
    message_id = data["message_id"]
    # message_id = request.json.get("message_id")  # retrieve message_id from JSON data
    print(message_id)

    with sqlite3.connect(get_db_path()) as conn:
        c = conn.cursor()

        # Check if the message exists before trying to delete
        c.execute(
            "SELECT * FROM FactConversation WHERE UserID = ? AND MessageID = ?",
            (UserID, message_id),
        )
        message = c.fetchone()
        if message is None:
            # Return an error if the message doesn't exist
            return jsonify({"error": "Message does not exist"}), 400

        # If the message exists, delete it
        try:
            c.execute(
                "UPDATE FactConversation SET MessageType = 0 WHERE UserID = ? AND MessageID = ?",
                (UserID, message_id),
            )
            conn.commit()
        except sqlite3.Error as e:
            print("Error:", e)

    conn.close()

    return jsonify({"success": True}), 200

