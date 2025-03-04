import sys
import os
from flask import request, jsonify, Blueprint


# Fixes issues with imports
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from db.user import (
    User,
    InvalidUserIDError,
)

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
                    "name": password.name,
                    "folder_name": password.folder_name,
                    "website": password.website,
                    "username": password.username,
                    "totp_secret": password.totp_secret,
                }
            )
        return jsonify(p)
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
    except:
        return jsonify(
            {"error": "INVALID_KEY_ENTERED", "text": "The key entered is incorrect"}
        )


@passwords.post("/api/user/<user_id>/password")
def add_password_route(user_id):
    key = request.args.get("key")
