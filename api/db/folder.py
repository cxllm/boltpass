import os
import sys

path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, path)
from database import connect
from password import Password


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
        self.get_passwords()

    def delete(self):
        conn, cursor = connect()
        passwords = self.get_passwords()
        for password in passwords:
            password.change_folder(None)
        cursor.execute(
            "DELETE FROM folders WHERE user_id = %s AND folder_name = %s",
            (self.user_id, self.folder_name),
        )
        conn.commit()
        conn.close()

    def get_passwords(self):
        conn, cursor = connect()
        cursor.execute(
            """SELECT password_id 
            FROM passwords
            WHERE user_id=%s AND folder_name=%s""",
            (self.user_id, self.folder_name),
        )
        password_ids = cursor.fetchall()
        conn.close()
        passwords = []
        for password_id in password_ids:
            passwords.append(Password(self.user_id, password_id))
        self.passwords = passwords
        return passwords


def create_folder(user_id, folder_name):
    folder_name = folder_name.capitalize()
    conn, cursor = connect()
    cursor.execute(
        "SELECT * FROM folders WHERE user_id = %s AND folder_name= %s",
        (user_id, folder_name),
    )
    out = cursor.fetchone()
    if out is not None:
        raise FolderAlreadyExistsError()
    cursor.execute("INSERT INTO folders VALUES (%s, %s)", (user_id, folder_name))
    conn.commit()
    return Folder(user_id, folder_name)
