from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import io

app = Flask(__name__)
socketio = SocketIO(app)

connected_ai_client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ai_status')
def ai_status():
    global connected_ai_client
    return jsonify({'ai_server_ip': connected_ai_client is not None})

@socketio.on('connect')
def handle_connect():
    emit('status', {'status': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    global connected_ai_client
    if connected_ai_client == request.sid:
        connected_ai_client = None
    emit('status', {'status': 'Disconnected from server'})

@socketio.on('register_ai')
def handle_register_ai():
    global connected_ai_client
    connected_ai_client = request.sid
    emit('status', {'status': 'AI server registered successfully'}, room=request.sid)

@socketio.on('process_video')
def handle_process_video(data):
    global connected_ai_client
    if connected_ai_client is None:
        emit('error', {'message': 'AI server is not available'})
        return
    
    socketio.emit('process_video', data, room=connected_ai_client)

@socketio.on('processed_video')
def handle_processed_video(data):
    emit('processed_video', data)
