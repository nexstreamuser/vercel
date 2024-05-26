from app import app
if __name__ == '__main__':
    socketio.run(app, port=5000)
