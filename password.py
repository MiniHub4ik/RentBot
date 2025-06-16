import os

PASSWORD_FILE = "password.txt"
OWNER_ID = 1686153131
authorized_users = {}

def load_password():
    """Loads the password from file or creates the file with a default password."""
    if not os.path.exists(PASSWORD_FILE):
        save_password("admin123")
    with open(PASSWORD_FILE, "r", encoding="utf-8") as file:
        return file.read().strip()

def save_password(new_password):
    """Saves the new password to the file."""
    with open(PASSWORD_FILE, "w", encoding="utf-8") as file:
        file.write(new_password)

def check_password(chat_id, user_input):
    """Checks the entered password."""
    return user_input == load_password()

def authorize_user(chat_id):
    """Adds the user to the list of authorized users."""
    authorized_users[chat_id] = True

def is_authorized(chat_id):
    """Checks if the user is authorized."""
    return chat_id in authorized_users

def change_password(new_password):
    """Changes the password and saves it to the file (for owner only)."""
    save_password(new_password)
