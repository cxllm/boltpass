import sys
import os
import json
import re

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Fixes issues with the hosting platform
# This code will be present in many files to combat these issues
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)

from util.generate_password import (
    password_generator,
    LengthTooLowError,
    LengthTooHighError,
)
from db.user import (
    User,
    create_user,
    EmailNotValidError,
    PasswordNotStrongEnoughError,
    EmailAlreadyExistsError,
    EmailNotRegisteredError,
    InvalidUserIDError,
)

# gets default values from the password generator function
default_length, default_uppercase, default_numbers, default_specialchars = (
    password_generator.__defaults__
)
# Regex to verify if the email is valid
emailRegex = r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
# Regex to verify if password is secure
passwordRegex = "^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^0-9A-Za-z]).{8,}$"

# initialise the flask application
app = Flask(
    __name__,
    static_folder=path + "/../frontend/dist",
    static_url_path="/",
    template_folder=path + "/../frontend/dist",
)
# Initliases CORS (Cross-Origin Resource Sharing) which allows the backend to be used within the frontend
CORS(app)


@app.get("/")
def root():
    # the root function sends the request to the frontend where it is handled accordingly
    return render_template("index.html")


@app.errorhandler(404)
def not_found(_=None):
    # Sends all pages that aren't covered by the backend to the frontend where it is handled accordingly
    return render_template("index.html")


@app.get("/api/generate-password")
def generate_password():
    try:
        # get the length and if it is invalid use the default length
        length = int(request.args.get("length", default=default_length))
    except:
        length = default_length
    # get uppercase parameter and if it is invalid use the default case
    uppercase = request.args.get("uppercase", default=default_uppercase)
    match uppercase:
        case "False":
            uppercase = False
        case "True":
            uppercase = True
        case _:
            uppercase = default_specialchars

    # get numbers parameter and if it is invalid use the default case
    numbers = request.args.get("numbers", default=default_numbers)
    match numbers:
        case "False":
            numbers = False
        case "True":
            numbers = True
        case _:
            numbers = default_specialchars

    # get special characters parameter and if it is invalid use the default case
    specialchars = request.args.get("specialchars", default=default_specialchars)
    match specialchars:
        case "False":
            specialchars = False
        case "True":
            specialchars = True
        case _:
            specialchars = default_specialchars
    try:
        # generate the password and return it in a json format
        return jsonify(
            {"password": password_generator(length, uppercase, numbers, specialchars)}
        )
    except LengthTooLowError:
        # return an error if it is too short
        return jsonify({"error": "The length of the password was not long enough"})
    except LengthTooHighError:
        # return an error if it is too long
        return jsonify({"error": "The length of the password was too long"})


@app.post("/api/sign-up")
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


@app.post("/api/login")
def login():
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
    # check that the email is valid and give an error if not
    if not re.match(emailRegex, email):
        return jsonify({"error": "INVALID_EMAIL", "text": "Email entered is invalid"})

    try:
        user = User(email_address=email)
        if not user.verify_password(password):
            return jsonify(
                {
                    "error": "PASSWORD_NOT_CORRECT",
                    "text": "The password entered is invalid",
                }
            )
        else:
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
        return jsonify(
            {"error": "EMAIL_NOT_REGISTERED", "text": "Email entered is not registered"}
        )


@app.get("/api/user/<user_id>")
def get_user_info(user_id):
    try:
        user = User(user_id=user_id)
        return jsonify(
            {
                "user_id": user.user_id,
                "email": user.email,
                "password_hash": user.password_hash,
                "salt": user.salt,
                "totp_enabled": user.totp_enabled,
                "totp_secret": user.totp_secret,
            }
        )
    except InvalidUserIDError:
        return jsonify(
            {"error": "USER_ID_INVALID", "text": "This user ID was not recognised."}
        )


# only run if the file is being called directly
if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0")
