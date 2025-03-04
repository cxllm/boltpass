import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from database import connect
from password import Password
from secure_notes import SecureNote


class FolderDoesNotExistError(Exception):
    pass


class FolderAlreadyExistsError(Exception):
    pass


class Folder:
    def __init__(self, user_id, folder_name):
        self.user_id = user_id
        self.folder_name = folder_name
        conn, cursor = connect()
        cursor.execute(
            "SELECT * FROM folders WHERE user_id=%s AND folder_name=%s",
            (self.user_id, self.folder_name),
        )
        out = cursor.fetchone()
        if out is None:
            raise FolderDoesNotExistError()
        conn.close()
        self.passwords = []
        self.secure_notes = []
        self.get_passwords()
        self.get_secure_notes()

    def delete(self):
        conn, cursor = connect()
        items = self.get_passwords() + self.get_secure_notes()
        for item in items:
            item.change_folder(None)
        cursor.execute(
            "DELETE FROM folders WHERE user_id = %s AND folder_name = %s",
            (self.user_id, self.folder_name),
        )
        conn.commit()
        conn.close()

    def get_passwords(self):
        conn, cursor = connect()
        cursor.execute(
            """SELECT password_id FROM passwords WHERE user_id=%s AND folder_name=%s"""
        )
        password_ids = cursor.fetchall()
        conn.close()
        passwords = []
        for password_id in password_ids:
            passwords.append(Password(self.user_id, password_id))
        self.passwords = passwords
        return passwords

    def get_secure_notes(self):
        conn, cursor = connect()
        cursor.execute(
            """SELECT note_id FROM secure_notes WHERE user_id=%s AND folder_name=%s"""
        )
        note_ids = cursor.fetchall()
        conn.close()
        secure_notes = []
        for note_id in note_ids:
            secure_notes.append(SecureNote(self.user_id, note_id))
        self.secure_notes = secure_notes
        return secure_notes


def create_folder(user_id, folder_name):
    conn, cursor = connect()
    cursor.execute(
        "SELECT * FROM folders WHERE user_id=%s, folder_name=%s", (user_id, folder_name)
    )
    out = cursor.fetchone()
    if out is not None:
        raise FolderAlreadyExistsError()
    cursor.execute("INSERT INTO folders VALUES (%s, %s)", (user_id, folder_name))
    conn.commit()
    return Folder(user_id, folder_name)
