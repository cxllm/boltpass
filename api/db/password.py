import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from database import connect
from util.encryption import decrypt


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
        ) = cursor.fetchone()
        conn.close()

    def decrypt(self, key):
        return decrypt(self.encrypted, self.salt, self.iv, key)
