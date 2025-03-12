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
    # Route to verify user email
    email = request.args.get("email")
    try:
        user = User(user_id=user_id)
        # Check that the email stored matches the one to be verified
        if user.email != email:
            return jsonify(
                {
                    "error": "EMAIL_DOES_NOT_MATCH",
                    "text": "Email does not match with the one being verified",
                }
            )
        # Verify the email if its not already (in case the link is pressed multiple times)
        if not user.email_verified:
            user.verify_email()
        # Redirect to the web page
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
    # Route to update a user's email
    # Requires password and new email to be entered
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
        # Verify that the password is correct
        if not user.verify_password(password):
            return jsonify(
                {
                    "error": "PASSWORD_NOT_CORRECT",
                    "text": "The password entered is invalid",
                }
            )
        # Ensure the new email is valid
        elif not re.match(emailRegex, email):
            return jsonify(
                {"error": "INVALID_EMAIL", "text": "Email entered is invalid"}
            )
        else:
            # Add the new email if its not already in use
            try:
                _ = User(email_address=email)
                return jsonify(
                    {"error": "EMAIL_IN_USE", "text": "Email is already in use"}
                )
            except EmailNotRegisteredError:
                # Add the new email if it isn't in use
                user.update_email(email)
                return jsonify({"success": True})
    # Catch for if user ID doesn't exist
    except InvalidUserIDError:
        return jsonify(
            {
                "error": "USER_ID_DOES_NOT_EXIST",
                "text": "The user ID entered is not valid",
            }
        )
