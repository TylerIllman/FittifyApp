from app.main import app
from flask_socketio import SocketIO


if __name__ == "__main__":
    socketio = SocketIO(app)
    socketio.run(app, port=5001, debug=True)
