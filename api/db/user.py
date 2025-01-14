import os
import sys
import uuid
import re

path = os.path.dirname(os.path.realpath(__file__ + "/.."))
sys.path.insert(1, path)
from util.password_hashing import verify_password, generate_hash

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)

from main import connect

# Regex to verify if the email is valid
emailRegex = r"^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
# Regex to verify if password is secure
passwordRegex = "^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[^0-9A-Za-z]).{8,}$"


# Error for when the email is already in use
class EmailAlreadyExistsError(Exception):
    pass


# Error for when the password is not strong enough
class PasswordNotStrongEnoughError(Exception):
    pass


# Error for when the email is invalid
class EmailNotValidError(Exception):
    pass


# Error for when the email is not registered
class EmailNotRegisteredError(Exception):
    pass


class User:
    def __init__(self, email_address="", user_id=""):
        # if neither email_address and user_id both have no value then throw an error
        if [email_address, user_id] in ["", ""]:
            raise ValueError("Either email_address or user_id needs to be provided!")
        # get a database connection
        conn, cursor = connect()
        # if the user id is entered then fetch the user from the database using this
        if user_id:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        # if the email is entered then fetch the user from the database using this
        elif email_address:
            cursor.execute(
                "SELECT * FROM users WHERE email_address = %s", (email_address,)
            )
        data = cursor.fetchone()
        if data is None:
            raise EmailNotRegisteredError()
        # put the data that is fetched from the database into the instance of the class
        self.user_id = data[0]
        self.email = data[1]
        self.password_hash = data[2]
        self.salt = data[3]
        self.totp_enabled = data[4]
        self.totp_secret = data[5]
        conn.commit()
        conn.close()

    # method to check if the password is correct
    def verify_password(self, password):
        return verify_password(password, self.salt, self.password_hash)


def create_user(email, password):
    # Check if email is valid and password is secure enough
    if not re.match(emailRegex, email):
        raise EmailNotValidError("Email is invalid")
    if not re.match(passwordRegex, password):
        raise PasswordNotStrongEnoughError(
            "Password does not meet security constraints"
        )
    # Get the database cursor
    conn, cursor = connect()
    # Check if a user with this email already exists
    cursor.execute("SELECT * FROM users WHERE email_address = %s", (email,))
    if cursor.fetchone() is not None:
        raise EmailAlreadyExistsError("This email already exists in the database")
    # generate a unique uuid as the user id
    user_id = str(uuid.uuid4())
    # generate the hashed password and salt
    hashed, salt = generate_hash(password)
    # insert these values into the database
    cursor.execute(
        """INSERT INTO users VALUES (
            %s, %s, %s, %s, %s, %s
        )""",
        (user_id, email, hashed, salt, False, None),
    )
    conn.commit()
    conn.close()
    # return the User class with the information that was just generated
    return User(email_address=email)
