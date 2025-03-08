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
from db.folder import Folder, FolderDoesNotExistError

folders = Blueprint("user_info", __name__)


@folders.get("/api/user/<user_id>/folders")
def user_folders_route(user_id):
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


@folders.delete("/api/user/<user_id>/folders/<folder_name>")
def user_folders_route(user_id, folder_name):
    try:
        user = User(user_id=user_id)
        folder = Folder(user_id, folder_name)
        folder.delete()
        return jsonify({"success": True})
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
    except FolderDoesNotExistError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )
