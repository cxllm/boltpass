import os
import sys
import uuid
import re

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from util.password_hashing import verify_password, generate_hash
from util.encryption import derive_key, encrypt
from util.smtp import verification_email
from util.security import check_instances_of_password, check_password_leaked
from folder import create_folder, Folder

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
    def __init__(self, email_address: str = "", user_id: str = "") -> None:
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
        self.email_verified = data[2]
        self.password_hash = data[3]
        self.salt = data[4]
        self.tfa_enabled = data[5]
        self.totp_secret = data[6]
        self.passwords = []
        self.recovery_codes = []
        self.folders = []
        self.get_passwords()
        self.get_recovery_codes()
        self.get_folders()

    # method to check if the password is correct
    def verify_password(self, password: str) -> bool:
        """
        Checks if the users password is correct
            Parameters:
                self: Refers to the specific instance of the class
                password (str): Password to verify
            Returns
                verified (bool): Whether or not the password is correct
        """
        return verify_password(password, self.salt, self.password_hash)

    def derive_key(self, password: str) -> str:
        """
        Derives the user's encryption key
            Parameters:
                self: Refers to the specific instance of the class
                password (str): Password to derive from
            Returns:
                key (str): The derived key in hex form
        """
        return derive_key(password, self.salt)[1]

    def update_password(self, old: str, new: str) -> None:
        """
        Update the user's password and all the passwords that have been encrypted
            Parameters:
                self: Refers to the specific instance of the class
                old (str): The old password
                new (str): The new password to update to
        """
        conn, cursor = connect()
        key = self.derive_key(old)  # Get the old encryption key
        hashed, salt = generate_hash(new)  # Get the new hash and salt for the new key
        cursor.execute(
            """UPDATE users 
            SET password_hash = %s, password_salt = %s
            WHERE user_id = %s""",
            (
                hashed,
                salt,
                self.user_id,
            ),  # Update the user's password hash in the database
        )
        conn.commit()
        conn.close()
        # Update this in the class
        self.password_hash = hashed
        self.salt = salt
        # Get the new key
        new_key = self.derive_key(new)
        for p in self.get_passwords():
            # Update each password individually with the new key
            decrypted = p.decrypt(key)
            p.update_password(decrypted, new_key)

    def send_verification_email(self) -> None:
        """
        Sends an email to the user to verify their email
        """
        verification_email(self.email, self.user_id)

    def verify_email(self) -> None:
        """
        Marks user's email as verified
        """
        self.email_verified = True
        conn, cursor = connect()
        cursor.execute(
            """UPDATE users
            SET email_verified = %s
            WHERE user_id = %s""",
            (self.email_verified, self.user_id),
        )
        conn.commit()
        conn.close()

    def update_email(self, email: str) -> None:
        """
        Update a user's email in the database and send a verification email to confirm
            Parameters:
                self: Refers to the specific instance of the class
                email (str): The email to update to
        """
        self.email_verified = False
        self.email = email
        conn, cursor = connect()
        cursor.execute(
            """UPDATE users
            SET email_verified = %s, email_address = %s
            WHERE user_id = %s""",
            (self.email_verified, self.email, self.user_id),
        )
        conn.commit()
        conn.close()
        self.send_verification_email()

    def add_password(
        self,
        name: str,
        password: str,
        key: str,
        username: str,
        website: str = None,
        totp_secret: str = None,
        folder_name: str = None,
    ) -> Password:
        """
        Add a password to the database
            Parameters:
                self: Refers to the specific instance of the class
                password (str): Password to encrypt
                key (str): Encryption key to use
            Returns:
                password (Password): The instance of the Password class for the password just added
        """
        # encrypt the password using AES
        encrypted, salt, iv = encrypt(password, key)
        # assign the password a random ID
        password_id = str(uuid.uuid4())
        # add to the database
        conn, cursor = connect()
        if folder_name:
            folder_name = folder_name.capitalize()
            cursor.execute(
                "SELECT * FROM folders WHERE folder_name = %s AND user_id = %s",
                (folder_name, self.user_id),
            )
            if cursor.fetchone() is None:
                create_folder(self.user_id, folder_name)
        cursor.execute(
            """INSERT INTO passwords VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""",
            (
                self.user_id,
                password_id,
                encrypted,
                salt,
                iv,
                username,
                name,
                folder_name,
                totp_secret,
                website,
            ),
        )
        conn.commit()
        conn.close()
        password = Password(user_id=self.user_id, password_id=password_id)
        # Add the new password into the instance of the class
        self.passwords.append(password)
        return password

    def get_passwords(self) -> list[Password]:
        """
        Gets all passwords from the database
            Parameters:
                self: Refers to the specific instance of the class

            Returns:
                passwords (Password[]): A list of the user's passwords, as instances of the Password class

        """
        conn, cursor = connect()
        # Get all the passwords IDs from the database
        cursor.execute(
            "SELECT password_id FROM passwords WHERE user_id = %s",
            (self.user_id,),
        )
        password_ids = cursor.fetchall()
        conn.close()
        # initialise a class for each passwords and put it in this class
        passwords = [
            Password(user_id=self.user_id, password_id=password[0])
            for password in password_ids
        ]
        self.passwords = passwords
        return passwords

    def check_security(self, key: str) -> dict[str, dict[str, int]]:
        """
        Check the security of the passwords by checking if there are repeeated entries or if there are leaked passwords

            Parameters:
                self: Refers to the specific instance of the class
                key (str): The encryption key to use to decrypt the passwords

            Returns:
                security (dict): The security information related to the user's stored passwords, including which passwords have been leaked or reused
        """
        self.get_passwords()
        counts = self.check_passwords_repeated(key)
        passwords = {}
        # Get all the passwords and decrypt them
        for password in self.passwords:
            decrypted = password.decrypt(key)
            passwords[decrypted] = {}
            # get how many times it was reused
            if decrypted in counts.keys():
                passwords[decrypted]["reused"] = counts[decrypted]
            # get how many times it was leaked
            passwords[decrypted]["leaked"] = check_password_leaked(decrypted)
        return passwords

    def check_passwords_repeated(self, key: str) -> dict[str, int]:
        """
        Check how many times the user has repeated a password

            Parameters:
                self: Refers to the specific instance of the class
                key (str): The user's encryption key

            Returns:
                counts (dict): How many times each password has been used
        """
        self.get_passwords()
        passwords = [p.decrypt(key) for p in self.passwords]
        counts = check_instances_of_password(passwords)
        return counts

    def get_recovery_codes(self) -> list[RecoveryCode]:
        """
        Get the users recovery codes

            Parameters:
                self: Refers to the specific instance of the class

            Returns:
                codes (RecoveryCode[]): The list of recovery codes
        """
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

    def get_folders(self) -> list[Folder]:
        """
        Get the users recovery folders

            Parameters:
                self: Refers to the specific instance of the class

            Returns:
                codes (RecoveryCode[]): The list of folders
        """
        conn, cursor = connect()
        cursor.execute(
            "SELECT folder_name FROM folders WHERE user_id = %s", (self.user_id,)
        )
        folders = cursor.fetchall()
        folders = [Folder(self.user_id, f[0]) for f in folders]
        conn.close()
        self.folders = folders
        return folders

    def disable_tfa(self) -> None:
        """
        Disable a user's Two Factor Authentication

            Parameters:
                self: Refers to the specific instance of the class
        """
        # Clear the values already stored in the class
        self.tfa_enabled = False
        self.totp_secret = None
        self.recovery_codes = []
        conn, cursor = connect()
        # Update in the database
        cursor.execute(
            """UPDATE users
                SET tfa_enabled = %s, totp_secret = %s
                WHERE user_id = %s
            """,
            (False, None, self.user_id),
        )
        # Delete corresponding recovery codes
        cursor.execute(
            """DELETE FROM recovery_codes WHERE user_id = %s""", (self.user_id,)
        )
        conn.commit()
        conn.close()

    def enable_tfa(self, totp_secret: str, recovery_codes: list[str]) -> None:
        """
        Enables 2FA for a user

            Parameters:
                self: Refers to the specific instance of the class
                totp_secret (str): The secret to add to the user
                recovery_codes (str[]): The recovery codes to correspond to the user
        """
        self.tfa_enabled = True
        self.totp_secret = totp_secret
        conn, cursor = connect()
        # Update values in the database
        cursor.execute(
            """UPDATE users
                SET tfa_enabled = %s, totp_secret = %s 
                WHERE user_id = %s""",
            (True, totp_secret, self.user_id),
        )
        # Add each recovery code to the database
        code_ids = []
        for code in recovery_codes:
            # They are each hashed instead of stored in plain text
            hashed, salt = generate_hash(code)
            # Assign each one a unique ID to form part of the primary key
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

    def check_recovery_code(self, to_verify: str) -> bool:
        """
        Checks if the user's entered recovery code is correct

            Parameters:
                self: Refers to the specific instance of the class
                to_verify (str): The code to verify

            Returns:
                valid (bool): If the code is correct
        """
        valid = False
        for code in self.recovery_codes:
            # Checks against each individual code
            check = code.verify(to_verify)
            if check:
                valid = True
                # Delete the code on use so that it can't be used again
                code.delete()
                # Break as the other codes don't need to be checked again
                break
        return valid


def create_user(email: str, password: str) -> User:
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
            %s, %s, %s, %s, %s, %s, %s
        )""",
        (user_id, email, False, hashed, salt, False, None),
    )
    conn.commit()
    conn.close()
    # return the User class with the information that was just generated
    return User(email_address=email)


def delete_user(user_id: str) -> bool:
    """
    Deletes a user from the database
        Parameters:
            user_id (str): The user ID to delete
    """
    # Delete user data and all data in other tables that is associated with that user
    # The user's info has to be deleted from the tables that depend on it first to not cause an error
    conn, cursor = connect()
    cursor.execute(
        """DELETE FROM recovery_codes
            WHERE user_id = %s""",
        (user_id,),
    )
    cursor.execute(
        """DELETE FROM passwords
            WHERE user_id = %s""",
        (user_id,),
    )
    cursor.execute(
        """DELETE FROM folders
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
