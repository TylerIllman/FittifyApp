from flask import Flask, redirect, url_for, render_template

from flask_socketio import SocketIO
import os
from datetime import timedelta

from .chatbot import chatbot_blueprint
from .signUp import signup_blueprint
from .login import login_blueprint
from .Personaldata import personalinfo_blueprint
from .savedMessages import saved_messages_blueprint

app = Flask(__name__)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

app = Flask(__name__)
app.config.from_pyfile("config.py")  # Load configuration from "config.py" file
app.config["DATABASE_URL"] = os.getenv("DATABASE_URL")  # Set the database URL from environment variable
app.secret_key = "BALLZ"  # Set a secret key for the application
socketio = SocketIO(app)  # Initialize SocketIO instance


# app.register_blueprint(main_blueprint)
app.register_blueprint(chatbot_blueprint)
app.register_blueprint(signup_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(personalinfo_blueprint)
app.register_blueprint(saved_messages_blueprint)

@app.route("/")
def root():
    return render_template("landingPage.html")  # Render "landingPage.html" template for the root route

if __name__ == "__main__":
    socketio.run(app, port=5001, debug=True)  # Run the application using SocketIO on port 5001 with debug mode enabled
