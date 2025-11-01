const socket = io();

let username;
let room;

function joinRoom() {
    username = document.getElementById('username').value;
    room = document.getElementById('room').value;
    if (username && room) {
        socket.emit('join', { username, room });
        document.getElementById('login').style.display = 'none';
        document.getElementById('chat').style.display = 'block';
    }
}

function sendMessage() {
    const msg = document.getElementById('message').value;
    if (msg) {
        socket.emit('message', { msg });
        document.getElementById('message').value = '';
    }
}

function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const filedata = e.target.result;
            socket.emit('upload', { filename: file.name, filedata: filedata.split(',')[1] });
        };
        reader.readAsDataURL(file);
        fileInput.value = '';
    }
}

function leaveRoom() {
    socket.emit('leave', { username, room });
    document.getElementById('chat').style.display = 'none';
    document.getElementById('login').style.display = 'block';
    document.getElementById('messages').innerHTML = '';
}

socket.on('message', function (data) {
    const messages = document.getElementById('messages');
    const msgDiv = document.createElement('div');
    msgDiv.innerHTML = `<strong>${data.username}</strong> [${data.timestamp}]: ${data.msg}`;
    messages.appendChild(msgDiv);
    messages.scrollTop = messages.scrollHeight;
});

socket.on('status', function (data) {
    const messages = document.getElementById('messages');
    const msgDiv = document.createElement('div');
    msgDiv.innerHTML = `<em>${data.msg}</em>`;
    messages.appendChild(msgDiv);
    messages.scrollTop = messages.scrollHeight;
});

// Request notification permission
if ('Notification' in window) {
    Notification.requestPermission();
}

socket.on('message', function (data) {
    // Show notification if not focused
    if (document.hidden && Notification.permission === 'granted') {
        new Notification(`New message from ${data.username}`, { body: data.msg });
    }
});