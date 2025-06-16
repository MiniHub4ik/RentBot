import json
import os

USERS_FILE = "users.json"

def load_users():
    """Loads the list of authorized users from the file."""
    if not os.path.exists(USERS_FILE):
        save_users({})
    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_users(users):
    """Saves the list of authorized users to the file."""
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

def authorize_user(chat_id, username):
    """Adds a user to the list of authorized users."""
    users = load_users()
    users[str(chat_id)] = username
    save_users(users)

def is_authorized(chat_id):
    """Checks if the user is authorized."""
    users = load_users()
    return str(chat_id) in users

def remove_user(chat_id):
    """Removes a user from the list of authorized users."""
    users = load_users()
    if str(chat_id) in users:
        del users[str(chat_id)]
        save_users(users)
        return True
    return False

def get_all_users():
    """Returns a list of all authorized users."""
    users = load_users()
    return users
