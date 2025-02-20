import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from database import connect
from util.password_hashing import verify_password


class RecoveryCode:
    def __init__(self, user_id, code_id):
        self.user_id = user_id
        self.code_id = code_id
        conn, cursor = connect()
        cursor.execute(
            "SELECT * FROM recovery_codes WHERE user_id=%s AND code_id=%s",
            (self.user_id, self.code_id),
        )
        (_, _, self.hashed, self.salt) = cursor.fetchone()
        conn.close()

    def verify(self, code):
        return verify_password(code, self.salt, self.hashed)
