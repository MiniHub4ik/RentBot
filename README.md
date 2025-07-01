# 🏠 Telegram Bot for Real Estate Listings

A Telegram bot for collecting and publishing real estate rental listings. Written in Python using `pyTelegramBotAPI`.

## 📌 Features

- Password protection for users  
- Admin password change feature  
- Supports multiple property types: House, Apartment, Room, Hotel  
- Step-by-step property submission  
- Photo uploads (multiple)  
- Auto-posts to a Telegram group

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- `pyTelegramBotAPI`  
  Install with:

```bash
pip install pyTelegramBotAPI
```

### Clone the Repository

```bash
git clone https://github.com/MiniHub4ik/your-repo-name.git
cd your-repo-name
```

### Configuration

Create the following files in the project directory:

#### `bot_token.py`
```python
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
```

#### `password.py`
```python
PASSWORD = "your_secret_password"
OWNER_ID = 123456789  # Replace with your Telegram ID

authorized_users = set()

def check_password(chat_id, entered_password):
    return entered_password == PASSWORD

def authorize_user(chat_id):
    authorized_users.add(chat_id)

def is_authorized(chat_id):
    return chat_id in authorized_users

def change_password(new_password):
    global PASSWORD
    PASSWORD = new_password
```

Replace the `GROUP_ID` in `main.py` with your own Telegram group ID.  
Make sure the bot is an **admin** in that group.

### Run the Bot

```bash
python main.py
```

## 📸 Usage Flow

1. User sends `/start`
2. Enters password
3. Fills out property form step by step
4. Uploads photos
5. Post is sent to the user and the group

## 🔑 Admin Controls

- The owner (`OWNER_ID`) sees a button to change the password from the main menu.

## 📂 Project Structure

```
├── bot_token.py
├── password.py
├── main.py
├── README.md
```

## 🛡 Security Note

This bot uses in-memory session and password handling.  
For production, consider:
- Persistent storage (e.g. Redis or a database)
- Hashed passwords (e.g. bcrypt)

## 🤝 Author

Made with ❤️ by Nematilla.\
Telegram: https://t.me/nematilla \
GitHub: https://github.com/MiniHub4ik
