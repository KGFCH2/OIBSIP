# 💬 ChatterLink - Chat Application

A comprehensive chat application project featuring both a beginner-friendly command-line version and an advanced browser-based version with modern features.

## 📋 Overview

ChatterLink provides two implementations of a real-time chat application:

1. **Basic Chat** - A simple text-based client-server application using Python sockets, perfect for learning networking concepts.
2. **Advanced Chat** - A feature-rich web-based application using Flask and SocketIO, offering a modern chat experience with multiple rooms, multimedia sharing, and more.

## ✨ Features

### Basic Chat
- 💻 Real-time text messaging via command line
- 🖧 Client-server architecture with threading
- 👥 Multiple clients can connect simultaneously
- 🪶 Simple and lightweight

### Advanced Chat
- 🌐 Web-based graphical user interface
- ⚡ Real-time messaging with WebSockets
- 🔐 User authentication (username-based)
- 🏠 Multiple chat rooms
- 📸 Multimedia sharing (image uploads)
- 📚 Message history (in-memory storage)
- 🔔 Browser notifications
- 😊 Emoji support (text-based)
- 📱 Responsive design

## 📁 Project Structure

```
ChatterLink/
├── basic_chat/
│   ├── server.py          # Server implementation for basic chat
│   ├── client.py          # Client implementation for basic chat
│   └── README.md          # Instructions for basic version
├── advanced_chat/
│   ├── app.py             # Flask application with SocketIO
│   ├── requirements.txt   # Python dependencies
│   ├── templates/
│   │   └── index.html     # Web interface template
│   ├── static/
│   │   ├── style.css      # CSS styling
│   │   └── script.js      # Client-side JavaScript
│   └── README.md          # Instructions for advanced version
└── README.md              # This file
```

## 🔧 How It Works

### Basic Chat
The basic version uses Python's built-in `socket` module to create a client-server architecture:

- **🖥️ Server** (`server.py`): Listens for incoming connections on port 5555, handles multiple clients using threading, and broadcasts messages to all connected clients.
- **💻 Client** (`client.py`): Connects to the server, sends user input as messages, and displays received messages in real-time.

Messages are exchanged as UTF-8 encoded strings over TCP connections.

### Advanced Chat
The advanced version uses Flask as the web framework and Flask-SocketIO for real-time communication:

- **⚙️ Backend** (`app.py`): Flask app with SocketIO integration handles WebSocket connections, room management, file uploads, and message broadcasting.
- **🖥️ Frontend**: HTML/CSS/JavaScript interface allows users to join rooms, send messages, upload images, and receive notifications.
- **⚡ Real-time Communication**: SocketIO enables instant message delivery without page refreshes.
- **📁 File Handling**: Images are uploaded to the server and served statically.

## 🚀 Installation and Setup

### Prerequisites
- 🐍 Python 3.x installed on your system

### Basic Chat Setup
1. Navigate to the `basic_chat` directory:
   ```bash
   cd basic_chat
   ```
2. No additional dependencies required - uses only Python standard library.

### Advanced Chat Setup
1. Navigate to the `advanced_chat` directory:
   ```bash
   cd advanced_chat
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

### Running Basic Chat
1. **▶️ Start the Server**:
   - Open a terminal and run: `python server.py`
   - The server will start listening on port 5555

2. **👥 Start Clients**:
   - Open additional terminals
   - In each terminal, run: `python client.py`
   - Enter messages to chat
   - Type 'quit' to exit

### Running Advanced Chat
1. **▶️ Start the Server**:
   ```bash
   python app.py
   ```
   The server will start on `http://127.0.0.1:5000/`

2. **🌐 Access the Chat**:
   - Open your web browser
   - Navigate to `http://127.0.0.1:5000/`
   - Enter a username and room name
   - Start chatting!

3. **✨ Features**:
   - Send text messages
   - Upload and share images
   - Use emojis in messages
   - Receive browser notifications for new messages
   - Join different rooms for separate conversations

## 🛠️ Technologies Used

### Basic Chat
- 🐍 Python 3.x
- 🔌 Socket programming (built-in `socket` module)
- 🧵 Threading (built-in `threading` module)

### Advanced Chat
- **⚙️ Backend**:
  - 🔥 Flask (web framework)
  - 🔌 Flask-SocketIO (real-time communication)
  - 🐍 Python-SocketIO (WebSocket support)
- **🖥️ Frontend**:
  - 🌐 HTML5
  - 🎨 CSS3
  - 💻 JavaScript (ES6+)
  - 🔌 Socket.IO client library

## 🔒 Security Considerations

- **Basic Chat**: No encryption - messages are sent in plain text. Suitable only for local testing.
- **Advanced Chat**: Basic implementation with username-based authentication. For production use, consider:
  - Proper user authentication system
  - Database storage instead of in-memory
  - Message encryption
  - Input validation and sanitization
  - Rate limiting

## 🚀 Future Improvements

- Add user registration and login system
- Implement persistent message storage (database)
- Add private messaging
- Implement end-to-end encryption
- Add video/voice calling capabilities
- Mobile-responsive design improvements
- Message reactions and threading
- File type validation and size limits
- Admin controls for room management

## 🤝 Contributing

Feel free to fork this project and add your own features or improvements. Make sure to test thoroughly and follow the existing code structure.

## 📄 License & Disclaimer

This project is developed as part of the **Oasis Infobyte Summer Internship Program (OIBSIP)** and is intended for educational and learning purposes only.

- The code is provided "as is" for educational reference.
- Commercial use is not permitted without explicit permission.
- All rights reserved to the original developer and Oasis Infobyte.