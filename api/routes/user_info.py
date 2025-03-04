import sys
import os
from flask import request, jsonify, Blueprint
from user_management import emailRegex


# Fixes issues with imports
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from db.user import (
    User,
    InvalidUserIDError,
)

user_info = Blueprint("user_info", __name__)


@user_info.get("/api/user/<user_id>/passwords")
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


@user_info.get("/api/user/<user_id>")
def user_info_route(user_id):
    try:
        user = User(user_id=user_id)
        return jsonify(
            {
                "user_id": user.user_id,
                "email": user.email,
                "email_verified": user.email_verified,
                "password_hash": user.password_hash,
                "salt": user.salt,
                "tfa_enabled": user.tfa_enabled,
                "totp_secret": user.totp_secret,
            }
        )
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
