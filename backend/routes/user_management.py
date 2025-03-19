import sys
import os
import json
import re

from flask import request, jsonify, Blueprint, redirect

# Fixes issues with imports
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)

user_management = Blueprint("user_management", __name__)

from db.user import (
    User,
    create_user,
    delete_user,
    EmailNotValidError,
    PasswordNotStrongEnoughError,
    EmailAlreadyExistsError,
    EmailNotRegisteredError,
    InvalidUserIDError,
)
from util.totp import verify

# Regex to verify if the email is valid
emailRegex = r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$"
# Regex to verify if password is secure
passwordRegex = r"^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^0-9A-Za-z]).{8,}$"


# Using POST to correspond to a CREATE command in SQL
@user_management.post("/api/sign-up")
def sign_up_route():
    # Route to sign up a new user
    # get the post request data
    data = json.loads(request.data)
    # make sure that both the email and password are in the request field
    if not ("email" in data.keys() and "password" in data.keys()):
        # return an error if not
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "Both username and password need to be included in the post request",
            }
        )
    email = data["email"]
    password = data["password"]
    # check that the email is valid and the password is secure enough and give an error if not
    if not re.match(emailRegex, email):
        return jsonify({"error": "INVALID_EMAIL", "text": "Email entered is invalid"})
    if not re.match(passwordRegex, password):
        return jsonify(
            {"error": "INVALID_PASSWORD", "text": "Password is not secure enough"}
        )
    try:
        # create a user with the details inputted
        user: User = create_user(email, password)
    except EmailAlreadyExistsError:
        # if the email is already in use, give an error
        return jsonify({"error": "EMAIL_IN_USE", "text": "Email is already in use"})
    except EmailNotValidError:
        # if the email is invalid, give an error
        return jsonify({"error": "INVALID_EMAIL", "text": "Email entered is invalid"})
    except PasswordNotStrongEnoughError:
        # if the password isn't strong enough give an error
        return jsonify(
            {"error": "INVALID_PASSWORD", "text": "Password is not secure enough"}
        )
    user.send_verification_email()
    # return the data given by the create_user function
    return jsonify(
        {
            "user_id": user.user_id,
            "email": user.email,
            "email_verified": user.email_verified,
            "password_hash": user.password_hash,
            "salt": user.salt,
            "tfa_enabled": user.tfa_enabled,
            "totp_secret": user.totp_secret,
            "key": user.derive_key(password),
        }
    )


# Using GET to correspond to a SELECT command in SQL
@user_management.get("/api/login")
def login_route():
    # Route to log the user in
    # get email and password from url query, and verifies if they have values
    email = request.args.get("email")
    password = request.args.get("password")
    if not email or not password:
        # return an error if not
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "Both username and password need to be included in the post request",
            }
        )
    # check that the email is valid and give an error if not
    if not re.match(emailRegex, email):
        return jsonify({"error": "INVALID_EMAIL", "text": "Email entered is invalid"})

    try:
        # Initialise the user class with the email
        user = User(email_address=email)
        # Make sure password is correct
        if not user.verify_password(password):
            return jsonify(
                {
                    "error": "PASSWORD_NOT_CORRECT",
                    "text": "The password entered is invalid",
                }
            )
        elif not user.email_verified:
            user.send_verification_email()
            return jsonify(
                {
                    "error": "USER_EMAIL_NOT_VERIFIED",
                    "text": "User email not verfied, user has been sent a verification email",
                }
            )

        else:
            # If password is correct, return their info with encryption key
            return jsonify(
                {
                    "user_id": user.user_id,
                    "email": user.email,
                    "email_verified": user.email_verified,
                    "password_hash": user.password_hash,
                    "salt": user.salt,
                    "tfa_enabled": user.tfa_enabled,
                    "totp_secret": user.totp_secret,
                    "key": user.derive_key(password),
                }
            )
    except EmailNotRegisteredError:
        # If the user doesn't exist
        return jsonify(
            {"error": "EMAIL_NOT_REGISTERED", "text": "Email entered is not registered"}
        )


@user_management.delete("/api/user/<user_id>")
def delete_user_route(user_id):
    # Route to delete a user account
    # Password is required to fulfill this request
    password = request.args.get("password")
    if not user_id or not password:
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "Both user id and password need to be included in the delete request",
            }
        )
    try:
        # Verify the user password
        user = User(user_id=user_id)
        if not user.verify_password(password):
            return jsonify(
                {
                    "error": "PASSWORD_NOT_CORRECT",
                    "text": "The password entered is invalid",
                }
            )
        if user.tfa_enabled:
            # Must enter 2fa code to verify
            totp_code = request.args.get("totp_code")
            recovery_code = request.args.get("recovery_code")
            if not totp_code and not recovery_code:
                return jsonify(
                    {
                        "error": "MISSING_DATA",
                        "text": "A totp code or recovery code is required for this account",
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

        return jsonify({"success": delete_user(user_id)})
    # Catch if user doesn't exist
    except InvalidUserIDError:
        return jsonify(
            {
                "error": "USER_ID_DOES_NOT_EXIST",
                "text": "The user ID entered is not valid",
            }
        )


@user_management.put("/api/user/<user_id>/2fa")
def update_2fa_route(user_id):
    password = request.args.get("password")
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
    except InvalidUserIDError:
        return jsonify(
            {
                "error": "USER_ID_DOES_NOT_EXIST",
                "text": "The user ID entered is not valid",
            }
        )


@user_management.get("/api/user/<user_id>/verify-recovery-code")
def verify_recovery_code_route(user_id):
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
        user = User(user_id=user_id)
        if not user.verify_password(password):
            return jsonify(
                {
                    "error": "PASSWORD_NOT_CORRECT",
                    "text": "The password entered is invalid",
                }
            )
        return jsonify(user.check_recovery_code(recovery_code))
    except InvalidUserIDError:
        return jsonify(
            {
                "error": "USER_ID_DOES_NOT_EXIST",
                "text": "The user ID entered is not valid",
            }
        )


@user_management.put("/api/user/<user_id>/password")
def update_user_password_route(user_id):
    # Route to update a user's password
    data = json.loads(request.data)
    # Must supply both old and new password
    if not user_id or "old" not in data.keys() or "new" not in data.keys():
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "User ID, old password and new password must be included in the request",
            }
        )
    try:
        # Ensure old password is correct first
        user = User(user_id=user_id)
        old = data["old"]
        new = data["new"]
        if not user.verify_password(old):
            return jsonify(
                {
                    "error": "PASSWORD_NOT_CORRECT",
                    "text": "The password entered is invalid",
                }
            )
        # Update after checking
        user.update_password(old, new)
        return jsonify({"success": True})

    # Catch in case user ID is invalid
    except InvalidUserIDError:
        return jsonify(
            {
                "error": "USER_ID_DOES_NOT_EXIST",
                "text": "The user ID entered is not valid",
            }
        )
