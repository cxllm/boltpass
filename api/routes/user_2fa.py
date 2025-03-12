import sys
import os
import json

from flask import request, jsonify, Blueprint

# Fixes issues with imports
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)

user_2fa = Blueprint("user_2fa", __name__)

from db.user import (
    User,
    InvalidUserIDError,
)
from util.totp import verify


@user_2fa.put("/api/user/<user_id>/2fa")
def update_2fa_route(user_id):
    # Route to update user's 2 Factor Authentication Settings
    # User must enter password to access this route
    password = request.args.get("password")
    # Get the request data which must have totp_secret and tfa_enabled in it
    data = json.loads(request.data)
    if (
        not password
        or not user_id
        or not ("totp_secret" in data.keys() and "tfa_enabled" in data.keys())
    ):
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "User ID, password and TOTP settings all need to be included in the put request",
            }
        )
    try:
        # verify the password is correct
        user = User(user_id=user_id)
        if not user.verify_password(password):
            return jsonify(
                {
                    "error": "PASSWORD_NOT_CORRECT",
                    "text": "The password entered is invalid",
                }
            )
        else:
            if data["tfa_enabled"]:
                # Add 2FA and the recovery codes codes
                if not "codes" in data.keys():
                    return jsonify(
                        {
                            "error": "MISSING_DATA",
                            "text": "Recovery codes need to be included in the put request",
                        }
                    )
                totp_secret = data["totp_secret"]
                recovery_codes = data["codes"]
                user.enable_tfa(totp_secret, recovery_codes)
                return jsonify({"enabled": True})
            else:
                # Disable it and verify that the TOTP code or recovery code entered is correct
                totp_code = request.args.get("totp_code")
                recovery_code = request.args.get("recovery_code")
                if not totp_code and not recovery_code:
                    return jsonify(
                        {
                            "error": "MISSING_DATA",
                            "text": "A totp code or recovery code must be included in the request",
                        }
                    )
                if totp_code:
                    if not verify(user.totp_secret, totp_code):
                        return jsonify(
                            {
                                "error": "TOTP_CODE_NOT_CORRECT",
                                "text": "The TOTP code entered is not correct",
                            }
                        )
                elif recovery_code:
                    if not user.check_recovery_code(recovery_code):
                        return jsonify(
                            {
                                "error": "RECOVERY_CODE_NOT_CORRECT",
                                "text": "The recovery code entered is not correct",
                            }
                        )
                user.disable_tfa()
                return jsonify({"enabled": False})
    # Catch if user doesn't exist
    except InvalidUserIDError:
        return jsonify(
            {
                "error": "USER_ID_DOES_NOT_EXIST",
                "text": "The user ID entered is not valid",
            }
        )


@user_2fa.get("/api/user/<user_id>/verify-recovery-code")
def verify_recovery_code_route(user_id):
    # User route to verify the recovery code
    # Needs a recovery code and a password to be entered
    recovery_code = request.args.get("recovery_code")
    password = request.args.get("password")
    if not user_id or not recovery_code or not password:
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "User ID, recovery code and password must be included in the request",
            }
        )
    try:
        # Check if the password is correct
        user = User(user_id=user_id)
        if not user.verify_password(password):
            return jsonify(
                {
                    "error": "PASSWORD_NOT_CORRECT",
                    "text": "The password entered is invalid",
                }
            )
        # Check the recovery code
        return jsonify(user.check_recovery_code(recovery_code))
    # Catch for if user doesn't exist
    except InvalidUserIDError:
        return jsonify(
            {
                "error": "USER_ID_DOES_NOT_EXIST",
                "text": "The user ID entered is not valid",
            }
        )
