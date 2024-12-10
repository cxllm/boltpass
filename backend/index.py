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
def root():
    return render_template("index.html")


@app.get("/api/generate-password")
def generate_password():
    try:
        length = int(request.args.get("length", default=default_length))
    except:
        length = default_length

    uppercase = request.args.get("uppercase", default=default_uppercase)
    match uppercase:
        case "False":
            uppercase = False
        case "True":
            uppercase = True
        case _:
            uppercase = default_specialchars

    numbers = request.args.get("numbers", default=default_numbers)
    match numbers:
        case "False":
            numbers = False
        case "True":
            numbers = True
        case _:
            numbers = default_specialchars

    specialchars = request.args.get("specialchars", default=default_specialchars)
    match specialchars:
        case "False":
            specialchars = False
        case "True":
            specialchars = True
        case _:
            specialchars = default_specialchars
    try:
        return jsonify(
            {"password": password_generator(length, uppercase, numbers, specialchars)}
        )
    except LengthTooLowError:
        return jsonify({"error": "The length of the password was not long enough"})
    except LengthTooHighError:
        return jsonify({"error": "The length of the password was too long"})


if __name__ == "__main__":
    app.run(port=3000)
