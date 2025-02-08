import sys
import os
import json
import re

from flask import request, jsonify, Blueprint

# Fixes issues with the hosting platform
# This code will be present in many files to combat these issues
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)

user_management = Blueprint("user_management", __name__)

from db.user import (
    User,
    create_user,
    EmailNotValidError,
    PasswordNotStrongEnoughError,
    EmailAlreadyExistsError,
    EmailNotRegisteredError,
)

# Regex to verify if the email is valid
emailRegex = r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
# Regex to verify if password is secure
passwordRegex = "^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^0-9A-Za-z]).{8,}$"


# Using POST to correspond to a CREATE command in SQL
@user_management.post("/api/sign-up")
def sign_up():
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
    # return the data given by the create_user function
    return jsonify(
        {
            "user_id": user.user_id,
            "email": user.email,
            "password_hash": user.password_hash,
            "salt": user.salt,
            "totp_enabled": user.totp_enabled,
            "totp_secret": user.totp_secret,
            "key": user.derive_key(password),
        }
    )


# Using GET to correspond to a SELECT command in SQL
@user_management.get("/api/login")
def login():
    # logs the user in
    referrer = request.referrer
    print(referrer)
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
        else:
            # If password is correct, return their info with encryption key
            return jsonify(
                {
                    "user_id": user.user_id,
                    "email": user.email,
                    "password_hash": user.password_hash,
                    "salt": user.salt,
                    "totp_enabled": user.totp_enabled,
                    "totp_secret": user.totp_secret,
                    "key": user.derive_key(password),
                }
            )
    except EmailNotRegisteredError:
        # If the user doesn't exist
        return jsonify(
            {"error": "EMAIL_NOT_REGISTERED", "text": "Email entered is not registered"}
        )
