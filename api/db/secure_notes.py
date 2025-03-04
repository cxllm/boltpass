import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from database import connect
from util.encryption import decrypt, encrypt


class SecureNote:
    def __init__(self, user_id, note_id):
        self.user_id = user_id
        self.note_id = note_id
        conn, cursor = connect()
        cursor.execute(
            "SELECT * FROM secure_notes WHERE user_id=%s AND password_id=%s",
            (self.user_id, self.note_id),
        )
        (
            _,
            _,
            self.encrypted,
            self.salt,
            self.iv,
            self.folder_name,
            self.name,
        ) = cursor.fetchone()
        conn.close()

    def decrypt(self, key):
        return decrypt(self.encrypted, self.salt, self.iv, key)

    def update(self, new_content, key):
        self.encrypted, self.salt, self.iv = encrypt(new_content, key)
        conn, cursor = connect()
        cursor.execute(
            """UPDATE secure_notes
            SET encrypted_data = %s, salt = %s, iv = %s
            WHERE note_id = %s, user_id = %s""",
            (self.encrypted, self.salt, self.iv, self.note_id, self.user_id),
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
            """UPDATE secure_notes
            SET folder_name=%s
            WHERE note_id=%s, user_id=%s""",
            (folder_name, self.note_id, self.user_id),
        )
        self.folder_name = folder_name
        conn.commit()
        conn.close()
        return self.folder_name

    def change_name(self, name):
        if not name:
            raise ValueError("Name needs to have a value")
        conn, cursor = connect()
        cursor.execute(
            """UPDATE secure_notes
            SET name=%s,
            WHERE note_id=%s, user_id=%s"""
        )
        self.name = name
        conn.commit()
        conn.close()
        return self.name
