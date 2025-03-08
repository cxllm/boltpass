import sys
import os
import json
import re

from flask import request, jsonify, Blueprint, redirect
from user_management import emailRegex

# Fixes issues with imports
path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)

user_email = Blueprint("user_email", __name__)

from db.user import User, InvalidUserIDError, EmailNotRegisteredError


@user_email.get("/api/user/<user_id>/verify-email")
def verify_user_email_route(user_id):
    email = request.args.get("email")
    try:
        user = User(user_id=user_id)
        if user.email != email:
            return jsonify(
                {
                    "error": "EMAIL_DOES_NOT_MATCH",
                    "text": "Email does not match with the one being verified",
                }
            )
        if not user.email_verified:
            user.verify_email()
        return redirect("/email-verified")
    except InvalidUserIDError:
        return jsonify(
            {
                "error": "USER_ID_DOES_NOT_EXIST",
                "text": "The user ID entered is not valid",
            }
        )


@user_email.put("/api/user/<user_id>/update-email")
def update_user_email_route(user_id):
    password = request.args.get("password")
    data = json.loads(request.data)
    if not password or not user_id or not "email" in data.keys():
        return jsonify(
            {
                "error": "MISSING_DATA",
                "text": "User ID, password and email all need to be included in the put request",
            }
        )
    try:
        email = data["email"]
        user = User(user_id=user_id)
        if not user.verify_password(password):
            return jsonify(
                {
                    "error": "PASSWORD_NOT_CORRECT",
                    "text": "The password entered is invalid",
                }
            )
        elif not re.match(emailRegex, email):
            return jsonify(
                {"error": "INVALID_EMAIL", "text": "Email entered is invalid"}
            )
        else:
            try:
                _ = User(email_address=email)
                return jsonify(
                    {"error": "EMAIL_IN_USE", "text": "Email is already in use"}
                )
            except EmailNotRegisteredError:
                user.update_email(email)
                return jsonify({"success": True})
    except InvalidUserIDError:
        return jsonify(
            {
                "error": "USER_ID_DOES_NOT_EXIST",
                "text": "The user ID entered is not valid",
            }
        )
