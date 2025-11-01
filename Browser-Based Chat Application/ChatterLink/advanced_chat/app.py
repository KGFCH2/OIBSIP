from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')

# In-memory storage for simplicity
users = {}  # sid: username
rooms = {}  # room: [messages]
current_rooms = {}  # sid: room

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    users[request.sid] = username
    current_rooms[request.sid] = room
    if room not in rooms:
        rooms[room] = []
    emit('status', {'msg': f'{username} has entered the room.'}, room=room)
    # Send message history
    for msg in rooms[room]:
        emit('message', msg, room=request.sid)

@socketio.on('leave')
def on_leave(data):
    username = users.get(request.sid, 'Unknown')
    room = current_rooms.get(request.sid, '')
    leave_room(room)
    emit('status', {'msg': f'{username} has left the room.'}, room=room)

@socketio.on('message')
def handle_message(data):
    username = users.get(request.sid, 'Unknown')
    room = current_rooms.get(request.sid, '')
    msg = {
        'username': username,
        'msg': data['msg'],
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    rooms[room].append(msg)
    emit('message', msg, room=room)

@socketio.on('upload')
def handle_upload(data):
    username = users.get(request.sid, 'Unknown')
    room = current_rooms.get(request.sid, '')
    filename = data['filename']
    filedata = data['filedata']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'wb') as f:
        f.write(filedata)
    msg = {
        'username': username,
        'msg': f'<img src="/static/uploads/{filename}" alt="image" style="max-width:200px;">',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    rooms[room].append(msg)
    emit('message', msg, room=room)

@socketio.on('disconnect')
def on_disconnect():
    username = users.pop(request.sid, 'Unknown')
    room = current_rooms.pop(request.sid, '')
    emit('status', {'msg': f'{username} has left the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)