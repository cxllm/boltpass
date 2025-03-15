import sys
import os

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Fixes issues with imports
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)

from util.generate_password import (
    password_generator,
    LengthTooLowError,
    LengthTooHighError,
)
from util.totp import verify as verify_totp, generate_totp, generate_code

# using blueprinting instead of putting all routes in one file to make the file neater
from routes.user_management import user_management
from routes.user_info import user_info
from routes.user_2fa import user_2fa
from routes.passwords import passwords
from routes.user_email import user_email
from routes.folders import folders

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
# Routes in a separate file to keep the main file uncluttered
app.register_blueprint(user_management)
app.register_blueprint(user_info)
app.register_blueprint(user_2fa)
app.register_blueprint(passwords)
app.register_blueprint(user_email)
app.register_blueprint(folders)


@app.get("/")
def root_route():
    # the root function sends the request to the frontend where it is handled accordingly
    return render_template("index.html")


@app.errorhandler(404)
def not_found_route(_=None):
    # Sends all pages that aren't covered by the backend to the frontend where it is handled accordingly
    return render_template("index.html")


@app.get("/api/generate-password")
def generate_password_route():
    # password generator api route
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


# Verify if the code enetered matches the secret at that point in time
@app.get("/api/verify-totp")
def verify_totp_route():
    # Gets code and secret from url query and ensures they have a value
    code = request.args.get("code")
    secret = request.args.get("secret")
    if not code and not secret:
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "Need a code and a secret",
            }
        )
    return jsonify(verify_totp(secret, code))


# Gets the code at this point in time for a specific secret
@app.get("/api/generate-totp-code")
def generate_totp_code_route():
    # Gets secret from url query and ensures it has a value
    secret = request.args.get("secret")
    if not secret:
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "Need a secret",
            }
        )
    return jsonify(generate_code(secret))


# generate TOTP config
@app.get("/api/generate-totp")
def generate_totp_route():
    # Gets name from url query and ensures it has a value
    name = request.args.get("name")
    if not name:
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "Need a name",
            }
        )
    # generate the secret and the QR code, and send it
    secret, image, codes = generate_totp(name)
    return jsonify(
        {
            "secret": secret,
            "image": f"data:image/png;base64,{image}",
            "recovery_codes": codes,
        }
    )


# only run if the file is being called directly
if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0", debug=True)
