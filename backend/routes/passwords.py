import sys
import os
import json
from flask import request, jsonify, Blueprint
from util.merge_sort import merge_sort

# Fixes issues with imports
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from db.user import (
    User,
    InvalidUserIDError,
)
from db.password import InvalidPasswordIDError, Password

passwords = Blueprint("passwords", __name__)


@passwords.get("/api/user/<user_id>/passwords")
def user_all_passwords_route(user_id):
    # Route to get a user's passwords
    # Cannot request without a user's key (which is required to be logged in)
    key = request.args.get("key")
    if not key:
        return jsonify(
            {"error": "NO_KEY_ENTERED", "text": "No encryption key was provided."}
        )
    try:
        user = User(user_id=user_id)
        # loop through each password and decrypt and send info to frontend
        passwords = user.get_passwords()
        p = []
        for password in passwords:
            decrypted = password.decrypt(key=key)
            p.append(
                {
                    "decrypted": decrypted,
                    "password_id": password.password_id,
                    "name": password.name,
                    "folder_name": password.folder_name,
                    "website": password.website,
                    "username": password.username,
                    "totp_secret": password.totp_secret,
                }
            )
        # Sort password by their name using merge sort
        p = merge_sort(p, "name")
        return jsonify(p)
    # Catch if user doesn't exist
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
    # Catch if there is an error decrypting passwords
    except:
        return jsonify(
            {"error": "INVALID_KEY_ENTERED", "text": "The key entered is incorrect"}
        )


@passwords.get("/api/user/<user_id>/password/<password_id>")
def user_password_route(user_id, password_id):
    # Route to get a specific password
    # Can't be accessed without an encryption key (as it is required to be logged in)
    key = request.args.get("key")
    if not key:
        return jsonify(
            {"error": "NO_KEY_ENTERED", "text": "No encryption key was provided."}
        )
    try:
        # Get the password from the database
        user = User(user_id=user_id)
        security = user.check_security(key)
        password = Password(user_id=user_id, password_id=password_id)
        decrypted = password.decrypt(key=key)
        # decrypt and send corresponding info to frontend, including breach and repeat data
        return jsonify(
            {
                "decrypted": decrypted,
                "password_id": password.password_id,
                "name": password.name,
                "folder_name": password.folder_name,
                "website": password.website,
                "username": password.username,
                "totp_secret": password.totp_secret,
                "reused": security[decrypted]["reused"],
                "leaked": security[decrypted]["leaked"],
            }
        )
    # Catch if user or password doesn't exist
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
    except InvalidPasswordIDError:
        return jsonify(
            {
                "error": "PASSWORD_ID_INVALID",
                "text": "This password ID was not recognised.",
            }
        )
    # Catch if the key is invalid
    except:
        return jsonify(
            {"error": "INVALID_KEY_ENTERED", "text": "The key entered is incorrect"}
        )


@passwords.post("/api/user/<user_id>/password")
def add_password_route(user_id):
    # Route to add a new password to the database
    # Key is required alongside the required values for a password to be stored in the database
    key = request.args.get("key")
    data = json.loads(request.data)
    keys = data.keys()
    if (
        not user_id
        or not key
        or not "password" in keys
        or not "username" in keys
        or not "name" in keys
    ):
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "Username, password, encryption key, user id and name need to be included in the post request",
            }
        )
    # Get all the data and ignore any that doesn't exist
    password = data["password"]
    username = data["username"]
    name = data["name"]
    website = data["website"] if data["website"] else None
    totp_secret = data["totp_secret"] if data["totp_secret"] else None
    folder_name = data["folder_name"].capitalize() if data["folder_name"] else None
    try:
        # Add password to database
        user = User(user_id=user_id)
        password = user.add_password(
            name, password, key, username, website, totp_secret, folder_name
        )
        return jsonify(
            {
                "decrypted": password.decrypt(key),
                "password_id": password.password_id,
                "name": password.name,
                "folder_name": password.folder_name,
                "website": password.website,
                "username": password.username,
                "totp_secret": password.totp_secret,
            }
        )
    # Catch if user doesn't exist
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )


@passwords.delete("/api/user/<user_id>/password/<password_id>")
def delete_password_route(user_id, password_id):
    # Route to delete a password from the database
    # Key is required to access this route (a requirement of being logged in)
    key = request.args.get("key")
    if not key:
        return jsonify(
            {"error": "NO_KEY_ENTERED", "text": "No encryption key was provided."}
        )
    try:
        _ = User(user_id=user_id)
        password = Password(user_id, password_id)
        password.decrypt(key)
        return jsonify(password.delete())
    # Catch if user or password doesn't exist
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
    except InvalidPasswordIDError:
        return jsonify(
            {
                "error": "PASSWORD_ID_INVALID",
                "text": "This password ID was not recognised.",
            }
        )
    # Catch if the key entered was wrong
    except:
        return jsonify(
            {"error": "INVALID_KEY_ENTERED", "text": "The key entered is incorrect"}
        )


@passwords.put("/api/user/<user_id>/password/<password_id>")
def edit_password_route(user_id, password_id):
    # Route to edit the information stored on the password in the database
    # Key is required to do this
    key = request.args.get("key")
    data = json.loads(request.data)
    keys = data.keys()
    if (
        not user_id
        or not password_id
        or not key
        or not "decrypted" in keys
        or not "username" in keys
        or not "name" in keys
    ):
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "Username, password, encryption key, user id, password id and name need to be included in the post request",
            }
        )
    try:
        # Get password information
        _ = User(user_id=user_id)
        password = Password(user_id, password_id)
        old = password.decrypt(key)
        new = data["decrypted"]
        username = data["username"]
        name = data["name"]
        # only update unrequired data if it has changed
        website = data["website"] if data["website"] else None
        totp_secret = data["totp_secret"] if data["totp_secret"] else None
        folder_name = data["folder_name"].capitalize() if data["folder_name"] else None
        # If the password has changed then update it
        if old != new:
            password.update_password(new, key)
        # Update the information
        password.update_information(name, username, website, totp_secret)
        # Update password if it has changed
        if folder_name != password.folder_name:
            password.change_folder(folder_name)
        # Update totp if it has changed
        if totp_secret != password.totp_secret:
            password.add_totp(totp_secret)
        # Return the updated information
        return jsonify(
            {
                "decrypted": password.decrypt(key),
                "password_id": password.password_id,
                "name": password.name,
                "folder_name": password.folder_name,
                "website": password.website,
                "username": password.username,
                "totp_secret": password.totp_secret,
            }
        )
    # Catch for if user doesn't exist
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
    # Catch for if password doesn't exist
    except InvalidPasswordIDError:
        return jsonify(
            {
                "error": "PASSWORD_ID_INVALID",
                "text": "This password ID was not recognised.",
            }
        )
    # Catch for wrong key
    except:
        return jsonify(
            {"error": "INVALID_KEY_ENTERED", "text": "The key entered is incorrect"}
        )


@passwords.get("/api/user/<user_id>/passwords/security")
def password_security_route(user_id):
    # Get the information on security of the users stored passwords
    # Key is required for this route
    key = request.args.get("key")
    if not key:
        return jsonify(
            {"error": "NO_KEY_ENTERED", "text": "No encryption key was provided."}
        )
    try:
        # get the amount of times a password has been leaked and repeated and return it in a dictionary
        user = User(user_id=user_id)
        security = user.check_security(key)
        passwords = user.get_passwords()
        p = []
        for password in passwords:
            decrypted = password.decrypt(key=key)
            p.append(
                {
                    "decrypted": decrypted,
                    "password_id": password.password_id,
                    "name": password.name,
                    "folder_name": password.folder_name,
                    "website": password.website,
                    "username": password.username,
                    "totp_secret": password.totp_secret,
                    "reused": security[decrypted]["reused"],
                    "leaked": security[decrypted]["leaked"],
                }
            )
        # Sort password by their name
        p = merge_sort(p, "name")
        return jsonify(p)
    # Catch for if route does not exist
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
    # Catch for if the key is invalid
    except:
        return jsonify(
            {"error": "INVALID_KEY_ENTERED", "text": "The key entered is incorrect"}
        )
