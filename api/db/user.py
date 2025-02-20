import os
import sys
import uuid
import re

path = os.path.dirname(os.path.realpath(__file__ + "/.."))
sys.path.insert(1, path)
from util.password_hashing import verify_password, generate_hash
from util.encryption import derive_key, encrypt

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from database import connect
from password import Password
from recovery_codes import RecoveryCode

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


# Error for when the User ID is not found
class InvalidUserIDError(Exception):
    pass


class User:
    def __init__(self, email_address="", user_id=""):
        """
        Constructor for the User class
            Parameters:
                self: Refers to the specific instance of the class
                email_address (str): The user's email address
                user_id (str): The user's unique ID
        """
        # if neither email_address and user_id both have no value then throw an error
        if [email_address, user_id] in ["", ""]:
            raise ValueError("Either email_address or user_id needs to be provided!")
        # get a database connection
        conn, cursor = connect()
        # if the user id is entered then fetch the user from the database using this
        if user_id:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            data = cursor.fetchone()
            if data is None:
                raise InvalidUserIDError()
        # if the email is entered then fetch the user from the database using this
        elif email_address:
            cursor.execute(
                "SELECT * FROM users WHERE email_address = %s", (email_address,)
            )
            data = cursor.fetchone()
            if data is None:
                raise EmailNotRegisteredError()
        conn.close()
        # put the data that is fetched from the database into the instance of the class
        self.user_id = data[0]
        self.email = data[1]
        self.password_hash = data[2]
        self.salt = data[3]
        self.tfa_enabled = data[4]
        self.totp_secret = data[5]
        self.passwords = []
        self.recovery_codes = []
        self.get_passwords()
        self.get_recovery_codes()

    # method to check if the password is correct
    def verify_password(self, password):
        """
        Checks if the users password is correct
            Parameters:
                self: Refers to the specific instance of the class
                password (str): Password to verify
            Returns
                verified (bool): Whether or not the password is correct
        """
        return verify_password(password, self.salt, self.password_hash)

    def derive_key(self, password):
        """
        Derives the user's encryption key
            Parameters:
                self: Refers to the specific instance of the class
                password (str): Password to derive from
            Returns
                key (str): The derived key in hex form
        """
        return derive_key(password, self.salt)[1]

    def add_password(
        self, name, password, key, website=None, totp_secret=None, folder_name=None
    ):
        """
        Add a password to the database
            Parameters:
                self: Refers to the specific instance of the class
                password (str): Password to encrypt
                key (str): Encryption key to use
        """
        # encrypt the password using AES
        encrypted, salt, iv = encrypt(password, key)
        # assign the password a random ID
        password_id = uuid.uuid4()
        # add to the database
        conn, cursor = connect()
        cursor.execute(
            """INSERT INTO password VALUES (
                %s, %s, %s, %s, %s, %s
            )""",
            (
                self.user_id,
                password_id,
                encrypted,
                salt,
                iv,
                folder_name,
                totp_secret,
                website,
                name,
            ),
        )
        conn.close()
        password = Password(user_id=self.user_id, password_id=password_id)
        self.passwords.append(password)
        return password

    def get_passwords(self):
        """
        Gets all passwords from the database
            Parameters:
                self: Refers to the specific instance of the class

            Returns:
                passwords (Password[]): A list of the user's passwords, as instances of the Password class

        """
        conn, cursor = connect()
        cursor.execute(
            "SELECT password_id FROM passwords WHERE user_id = %s",
            (self.user_id,),
        )
        password_ids = cursor.fetchall()
        conn.close()
        passwords = [
            Password(user_id=self.user_id, password_id=password[0])
            for password in password_ids
        ]
        self.passwords = passwords
        return passwords

    def get_recovery_codes(self):
        conn, cursor = connect()
        cursor.execute(
            "SELECT code_id FROM recovery_codes WHERE user_id = %s",
            (self.user_id,),
        )
        code_ids = cursor.fetchall()
        conn.close()
        codes = [
            RecoveryCode(user_id=self.user_id, code_id=code[0]) for code in code_ids
        ]
        self.recovery_codes = codes
        return codes

    def disable_tfa(self):
        self.tfa_enabled = False
        self.totp_secret = None
        self.recovery_codes = []
        conn, cursor = connect()
        cursor.execute(
            """UPDATE users
                SET tfa_enabled = %s, totp_secret = %s
                WHERE user_id = %s
            """,
            (False, None, self.user_id),
        )
        cursor.execute(
            """DELETE FROM recovery_codes WHERE user_id = %s""", (self.user_id,)
        )
        conn.commit()
        conn.close()

    def enable_tfa(self, totp_secret, recovery_codes):
        self.tfa_enabled = True
        self.totp_secret = totp_secret
        conn, cursor = connect()
        cursor.execute(
            """UPDATE users
                SET tfa_enabled = %s, totp_secret = %s 
                WHERE user_id = %s""",
            (True, totp_secret, self.user_id),
        )
        code_ids = []
        for code in recovery_codes:
            hashed, salt = generate_hash(code)
            code_id = str(uuid.uuid4())
            code_ids.append(code_id)
            cursor.execute(
                "INSERT INTO recovery_codes VALUES (%s, %s, %s, %s)",
                (self.user_id, code_id, hashed, salt),
            )
        conn.commit()
        conn.close()
        self.recovery_codes = [
            RecoveryCode(self.user_id, code_id) for code_id in code_ids
        ]

    def check_recovery_code(self, to_verify):
        valid = False
        for code in self.recovery_codes:
            check = code.verify(to_verify)
            if check:
                valid = True
                code.delete()
                break
        return valid


def create_user(email, password):
    """
    Adds a user to a database if they don't already exist
        Parameters:
            email (str): The user's email
            password (str): The user's password
        Returns
            user (User): An instance of the User class built for that new user.
    """
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


def delete_user(user_id):
    """
    Deletes a user from the database
        Parameters:
            user_id (str): The user ID to delete
    """
    # Delete user data and all data in other tables that is associated with that user
    conn, cursor = connect()
    cursor.execute(
        """DELETE FROM recovery_codes
            WHERE user_id = %s""",
        (user_id,),
    )
    cursor.execute(
        """DELETE FROM folders
            WHERE user_id = %s""",
        (user_id,),
    )
    cursor.execute(
        """DELETE FROM passwords
            WHERE user_id = %s""",
        (user_id,),
    )
    cursor.execute(
        """DELETE FROM secure_notes
            WHERE user_id = %s""",
        (user_id,),
    )
    cursor.execute(
        """DELETE FROM users 
            WHERE user_id = %s""",
        (user_id,),
    )

    cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    out = cursor.fetchone()
    conn.commit()
    conn.close()
    return out is None
