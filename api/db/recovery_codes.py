import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from database import connect
from util.password_hashing import verify_password


class RecoveryCode:
    def __init__(self, user_id: str, code_id: str) -> None:
        """
        Initialises the recovery code class

            Parameters:
                self: The specific instance of the class
                user_id (str): The user ID associated with the code
                code_id (str): The code ID associated with the code
        """
        self.user_id = user_id
        self.code_id = code_id
        # Get information from database. Verification not needed as it will only be called in a context where it is known to exist.
        conn, cursor = connect()
        cursor.execute(
            "SELECT * FROM recovery_codes WHERE user_id=%s AND code_id=%s",
            (self.user_id, self.code_id),
        )
        (_, _, self.hashed, self.salt) = cursor.fetchone()
        conn.close()

    def verify(self, code):
        """
        Verify if a recovery code entered is the right code

            Parameters:
                self: The specific instance of the class
                code (str): The code to verify

            Returns:
                out (bool): Whether the code is correct or not
        """
        return verify_password(code, self.salt, self.hashed)

    def delete(self):
        """
        Deletes a recovery code

            Parameters:
                self: The specific instance of the class
        """
        conn, cursor = connect()
        cursor.execute(
            "DELETE FROM recovery_codes WHERE user_id = %s AND code_id = %s",
            (self.user_id, self.code_id),
        )
        conn.commit()
        conn.close()
