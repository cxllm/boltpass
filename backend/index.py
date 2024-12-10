import sys
import os

# to ensure that the vercel deployment works
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)))

from flask import Flask, request, jsonify, render_template
from util.generate_password import (
    password_generator,
    LengthTooLowError,
    LengthTooHighError,
)

default_length, default_uppercase, default_numbers, default_specialchars = (
    password_generator.__defaults__
)


# initialise the flask application
app = Flask(
    __name__,
    static_folder="../frontend/dist",
    static_url_path="/",
    template_folder="../frontend/dist",
)


@app.get("/")
@app.errorhandler(404)
def root():
    # the root function sends all requests at the root or an unknown page to react, which will handle it from there
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


if __name__ == "__main__":
    app.run(port=3000)
