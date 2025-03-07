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
def user_passwords_route(user_id):
    key = request.args.get("key")
    if not key:
        return jsonify(
            {"error": "NO_KEY_ENTERED", "text": "No encryption key was provided."}
        )
    try:
        user = User(user_id=user_id)
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
        # Sort password by their name
        p = merge_sort(p, "name")
        return jsonify(p)
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
    except:
        return jsonify(
            {"error": "INVALID_KEY_ENTERED", "text": "The key entered is incorrect"}
        )


@passwords.get("/api/user/<user_id>/password/<password_id>")
def user_password_route(user_id, password_id):
    key = request.args.get("key")
    if not key:
        return jsonify(
            {"error": "NO_KEY_ENTERED", "text": "No encryption key was provided."}
        )
    try:
        _ = User(user_id=user_id)
        password = Password(user_id=user_id, password_id=password_id)
        decrypted = password.decrypt(key=key)
        return jsonify(
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
    except:
        return jsonify(
            {"error": "INVALID_KEY_ENTERED", "text": "The key entered is incorrect"}
        )


@passwords.post("/api/user/<user_id>/password")
def add_password_route(user_id):
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
                "text": "Both username, password, encryption key, user id and name need to be included in the post request",
            }
        )
    password = data["password"]
    username = data["username"]
    name = data["name"]
    website = data["website"] if data["website"] else None
    totp_secret = data["totp_secret"] if data["totp_secret"] else None
    folder_name = data["folder_name"].capitalize() if data["folder_name"] else None
    try:
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
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )


@passwords.delete("/api/user/<user_id>/password/<password_id>")
def delete_password_route(user_id, password_id):
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
    except:
        return jsonify(
            {"error": "INVALID_KEY_ENTERED", "text": "The key entered is incorrect"}
        )


@passwords.put("/api/user/<user_id>/password/<password_id>")
def edit_password_route(user_id, password_id):
    pass
