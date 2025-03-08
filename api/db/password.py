import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from database import connect
from util.encryption import decrypt, encrypt
from util.totp import generate_code


class InvalidPasswordIDError(Exception):
    pass


class Password:
    def __init__(self, user_id: str, password_id: str) -> None:
        """
        Initialise the password class

            Parameters:
                self: The specific instance of the class
                user_id (str): The user ID associated with the password
                password_id (str): The password ID for the password
        """
        self.user_id = user_id
        self.password_id = password_id
        conn, cursor = connect()
        # Get info from database
        cursor.execute(
            "SELECT * FROM passwords WHERE user_id=%s AND password_id=%s",
            (self.user_id, self.password_id),
        )
        data = cursor.fetchone()
        # If password doesn't exist then throw an error
        if data is None:
            raise InvalidPasswordIDError
        # Set the properties of the class
        (
            _,
            _,
            self.encrypted,
            self.salt,
            self.iv,
            self.username,
            self.name,
            self.folder_name,
            self.totp_secret,
            self.website,
        ) = data
        conn.close()

    def decrypt(self, key: str) -> tuple[str]:
        """
        Decrypt the password

            Parameters:
                self: The specific instance of the class
                key (str): The encryption key to decrypt with

            Returns:
                decrypted (str): The decrypted password
        """
        return decrypt(self.encrypted, self.salt, self.iv, key)

    def add_totp(self, secret: str) -> None:
        """
        Add a time-based one-time password secret to the password

            Parameters:
                self: The specific instance of the class
                secret (str): The secret to add
        """
        self.totp_secret = secret
        conn, cursor = connect()
        # Update the password record in the database
        cursor.execute(
            """UPDATE passwords
            SET totp_secret = %s
            WHERE password_id = %s, user_id = %s""",
            (self.totp_secret, self.password_id, self.user_id),
        )
        conn.commit()
        conn.close()

    def generate_totp(self) -> str:
        """
        Generates a TOTP code for this password

            Returns:
                code (str): The generated code
        """
        return generate_code(self.totp_secret)

    def update_password(self, new_password: str, key: str) -> tuple[str]:
        """
        Updates the password to a new value

            Parameters
                self: The specific instance of the class
                new_password (str): The password to update to
                key (str): The key to encrypt using

            Returns:
                encrypted (str): The encrypted password
                salt (str): The salt the password was encrypted with
                iv (str): The initialisation vector the password was encrypted with

        """
        # Generate the new password's encryption details
        self.encrypted, self.salt, self.iv = encrypt(new_password, key)
        conn, cursor = connect()
        # Update the database
        cursor.execute(
            """UPDATE passwords
            SET encrypted_password = %s, salt = %s, iv = %s
            WHERE password_id = %s AND user_id = %s""",
            (self.encrypted, self.salt, self.iv, self.password_id, self.user_id),
        )
        conn.commit()
        conn.close()
        return (self.encrypted, self.salt, self.iv)

    def change_folder(self, folder_name: str = None) -> str:
        """
        Update the folder a password is in

            Parameters:
                self: The specific instance of the class
                folder_name (str): The folder to update to

            Returns:
                folder_name (str): The folder updated to
        """
        conn, cursor = connect()
        # If the folder does not exist, create the folder
        if folder_name:
            folder_name = folder_name.capitalize()
            cursor.execute(
                """SELECT * FROM folders WHERE user_id=%s AND folder_name=%s""",
                (self.user_id, folder_name),
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    """INSERT INTO folders VALUES (%s, %s)""",
                    (self.user_id, folder_name),
                )
        # Update the new folder name in the database
        cursor.execute(
            """UPDATE passwords
            SET folder_name=%s
            WHERE password_id=%s AND user_id=%s""",
            (folder_name, self.password_id, self.user_id),
        )
        # If the password was previously in a folder and it was the only member, delete this folder as it is now empty
        if self.folder_name:
            cursor.execute(
                """SELECT * FROM passwords WHERE user_id=%s AND folder_name=%s""",
                (self.user_id, self.folder_name),
            )
            data = cursor.fetchall()
            if len(data) == 0:
                cursor.execute(
                    "DELETE FROM folders WHERE user_id=%s AND folder_name=%s",
                    (self.user_id, self.folder_name),
                )
        self.folder_name = folder_name
        conn.commit()
        conn.close()
        return self.folder_name

    def update_information(
        self,
        name: str,
        username: str,
        website: str = None,
        totp_secret: str = None,
    ):
        """
        Update the information associated with the password

            Parameters:
                self: The specific instance of the class
                name (str): The new reference name for the password
                username (str): The new username for the password
                website (str): The new website name for the password
                totp_secret (str): The new TOTP secret for the password

            Returns:
                name (str): The new reference name for the password
                username (str): The new username for the password
                website (str): The new website name for the password
                totp_secret (str): The new TOTP secret for the password
        """
        # If no changes are made, don't do anything
        if (
            website is None
            and name is None
            and totp_secret is None
            and username is None
        ):
            pass
        # If the changed values are the same as the existing ones, don't do anything
        elif (
            website == self.website
            and name == self.name
            and totp_secret == self.totp_secret
            and username == self.username
        ):
            pass
        else:
            # Update the values that have been changed
            self.website = website if website else self.website
            self.name = name if name else self.name
            self.totp_secret = totp_secret if totp_secret else self.totp_secret
            self.username = username if username else self.username
            # Update in database
            conn, cursor = connect()
            cursor.execute(
                """UPDATE passwords
                SET name=%s, website=%s, totp_secret=%s, username=%s
                WHERE password_id=%s AND user_id=%s""",
                (
                    self.name,
                    self.website,
                    self.totp_secret,
                    self.username,
                    self.password_id,
                    self.user_id,
                ),
            )
            conn.commit()
            conn.close()
        return self.website, self.name, self.totp_secret, self.username

    def delete(self):
        conn, cursor = connect()

        cursor.execute(
            """DELETE FROM passwords WHERE password_id = %s AND user_id = %s""",
            (self.password_id, self.user_id),
        )
        if self.folder_name:
            cursor.execute(
                """SELECT * FROM passwords WHERE folder_name = %s AND user_id = %s""",
                (self.folder_name, self.user_id),
            )
            if len(cursor.fetchall()) == 0:
                # If this password is the last one in the folder, delete the folder
                cursor.execute(
                    """DELETE FROM folders WHERE folder_name = %s AND user_id = %s""",
                    (self.folder_name, self.user_id),
                )
        cursor.execute(
            """SELECT * FROM passwords WHERE password_id = %s AND user_id = %s""",
            (self.password_id, self.user_id),
        )
        out = cursor.fetchone()
        conn.commit()
        conn.close()
        return out is None
