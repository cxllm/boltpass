import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from database import connect
from util.encryption import decrypt, encrypt
from util.totp import generate_code


class Password:
    def __init__(self, user_id, password_id):
        self.user_id = user_id
        self.password_id = password_id
        conn, cursor = connect()
        cursor.execute(
            "SELECT * FROM passwords WHERE user_id=%s AND password_id=%s",
            (self.user_id, self.password_id),
        )
        (
            _,
            _,
            self.encrypted,
            self.salt,
            self.iv,
            self.folder_name,
            self.totp_secret,
            self.website,
            self.name,
            self.username,
        ) = cursor.fetchone()
        conn.close()

    def decrypt(self, key):
        return decrypt(self.encrypted, self.salt, self.iv, key)

    def add_totp(self, secret):
        self.totp_secret = secret
        conn, cursor = connect()
        cursor.execute(
            """UPDATE passwords
            SET totp_secret = %s
            WHERE password_id = %s, user_id = %s""",
            (self.totp_secret, self.password_id, self.user_id),
        )
        conn.commit()
        conn.close()

    def generate_totp(self):
        return generate_code(self.totp_secret)

    def update_password(self, new_password, key):
        self.encrypted, self.salt, self.iv = encrypt(new_password, key)
        conn, cursor = connect()
        cursor.execute(
            """UPDATE passwords
            SET encrypted_password = %s, salt = %s, iv = %s
            WHERE password_id = %s, user_id = %s""",
            (self.encrypted, self.salt, self.iv, self.password_id, self.user_id),
        )
        conn.commit()
        conn.close()
        return (self.encrypted, self.salt, self.iv)

    def change_folder(self, folder_name=None):
        conn, cursor = connect()
        if folder_name:
            cursor.execute(
                """SELECT * FROM folders WHERE user_id=%s, folder_name=%s""",
                (self.user_id, folder_name),
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    """INSERT INTO folders VALUES (%s, %s)""",
                    (self.user_id, folder_name),
                )
        cursor.execute(
            """UPDATE passwords
            SET folder_name=%s
            WHERE password_id=%s, user_id=%s""",
            (folder_name, self.password_id, self.user_id),
        )
        self.folder_name = folder_name
        conn.commit()
        conn.close()
        return self.folder_name

    def update_information(
        self, website=None, name=None, totp_secret=None, username=None
    ):
        if (
            website is None
            and name is None
            and totp_secret is None
            and username is None
        ):
            pass
        else:
            self.website = website if website else self.website
            self.name = name if name else self.name
            self.totp_secret = totp_secret if totp_secret else self.totp_secret
            self.username = username if username else self.username
            conn, cursor = connect()
            cursor.execute(
                """UPDATE passwords
                SET name=%s, website=%s, totp_secret=%s, username=%s
                WHERE password_id=%s, user_id=%s""",
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
