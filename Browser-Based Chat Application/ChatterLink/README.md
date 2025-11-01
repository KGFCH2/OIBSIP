# ChatterLink

ChatterLink is a demo real-time chat application built with Flask, Flask-SocketIO, and SQLite. It demonstrates user registration/login, chat rooms, private messaging, media uploads, and message encryption at rest using Fernet.

## What you get
- Flask backend with Socket.IO real-time updates
- User registration/login (Flask-Login)
- Multiple chat rooms and message history
- File uploads (images/videos)
- Message encryption at rest using cryptography.Fernet
- Typing indicators and simple online presence

## Quick setup (Windows / VS Code)

1. Open the project folder in VS Code.
2. Create a virtual environment and activate it (cmd.exe):

```cmd
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```cmd
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and tweak if desired. At minimum set SECRET_KEY and FERNET_KEY for production.

Important security note: Do NOT commit a real `.env` file containing secrets to version control. The repository includes a `.gitignore` (added to the project) which ignores `.env` and other local/runtime artifacts. For deployment, set secrets via your hosting platform's secret manager (for example Render/Heroku/Streamlit Cloud config vars) or keep a local `.env` only on your machine.

5. Run the app:

```cmd
python app.py
```

Open http://localhost:5000 in your browser.

## Notes and security
- Messages are encrypted at rest using Fernet. The app encrypts messages before saving to the DB and stores ciphertext in the `messages` table. The server decrypts when serving message history. This protects stored data, but is not full end-to-end encryption.
- For real end-to-end encryption, encrypt/decrypt on the client and never send plaintext to the server.
- In production: set a persistent `FERNET_KEY` in environment variables, use HTTPS, and use a production DB (MySQL/Postgres).
- Use strong secret keys and configure CORS and session cookie security.

## Example encryption snippet

```py
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(b"Hello from ChatterLink")
decrypted = cipher.decrypt(encrypted)
print(decrypted.decode())
```

## Deployment hints
- Use a WSGI server that supports async (eventlet/gevent) when using Flask-SocketIO. For example, include `eventlet` and run with `socketio.run(app, host='0.0.0.0', port=5000)`.
- For platforms like Render/Heroku: set environment variables (SECRET_KEY, FERNET_KEY, DATABASE_URL). Use a managed DB for production.
