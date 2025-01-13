import hashlib
import os


def generate_hash(password: str) -> tuple[str, str]:
    """
    Generates a password hash and salt to securely store the master password in the database

        Parameters:
            password (str): The password to be hashed

        Returns:
            hashed_passsword (str): The hash string of the password entered
            salt (str): The salt that has
    """
    salt = os.urandom(32).hex()
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
    return hashed_password, salt


def verify_password(password: str, salt: str, hashed: str) -> bool:
    """
    Verifies if the password and the salt entered match the previously stored value

        Paramaters:
            password (str): The password to be verified
            salt (str): The salt that the password is to be added with
            hashed (str): The hash string that is already stored in the database to compare against

        Returns:
            condition (bool): Whether or not the password matches
    """
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
    return hashed_password == hashed
