import sys
import os
from flask import jsonify, Blueprint


# Fixes issues with imports
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from db.user import (
    User,
    InvalidUserIDError,
)

user_info = Blueprint("user_info", __name__)


@user_info.get("/api/user/<user_id>")
def user_info_route(user_id):
    # Route to get user info if the ID exists
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


@user_info.get("/api/user/<user_id>/folders")
def user_folders_route(user_id):
    # Get all the user's folders if the user exists
    try:
        user = User(user_id=user_id)
        folders = [
            {
                "user_id": f.user_id,
                "folder_name": f.folder_name,
                "items": len(f.get_passwords()),
            }
            for f in user.folders
        ]
        return jsonify(folders)
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
