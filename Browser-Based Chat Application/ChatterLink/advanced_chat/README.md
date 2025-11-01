# Advanced Chat Application - README

## Description
An advanced browser-based chat application built with Flask and SocketIO. Features include user authentication, multiple chat rooms, multimedia sharing, message history, notifications, and emojis.

## Features
- Real-time messaging with SocketIO
- User authentication (username-based)
- Multiple chat rooms
- Image upload and sharing
- Message history (in-memory)
- Browser notifications
- Emojis support (text-based)
- Responsive web interface

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Open your browser to `http://127.0.0.1:5000/`
4. Join a room and start chatting!

## Requirements
- Python 3.x
- Flask
- Flask-SocketIO
- python-socketio

## Usage
- Enter username and room name to join.
- Type messages and send.
- Upload images to share.
- Use text emojis like 😀.
- Leave room when done.

## Security Note
This is a basic implementation. For production, add proper authentication, database storage, and encryption.