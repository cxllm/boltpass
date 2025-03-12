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
    def __init__(self, user_id: str, folder_name: str) -> None:
        """
        Initialises the Folder class

            Parameters:
                self: The specific instance of the class
                user_id (str): The user ID associated with the folder
                folder_name (str): The name of the folder
        """
        # Set properties of class
        self.user_id = user_id
        self.folder_name = folder_name
        conn, cursor = connect()
        # Check if the folder exists in database, and raise an error if not
        cursor.execute(
            "SELECT * FROM folders WHERE user_id=%s AND folder_name=%s",
            (self.user_id, self.folder_name),
        )
        out = cursor.fetchone()
        if out is None:
            raise FolderDoesNotExistError()
        conn.close()
        # Get the passwords that are linked to this folder
        self.passwords = []
        self.get_passwords()

    def delete(self) -> None:
        """
        Deletes the folder

            Parameters:
                self: The specific instance of the class
        """
        conn, cursor = connect()
        passwords = self.get_passwords()
        for password in passwords:
            # Changes folder on all passwords that link as the folder cannot be deleted while there are records that have its primary key as a foreign key
            password.change_folder(None)
        # Deletes folder from database
        cursor.execute(
            "DELETE FROM folders WHERE user_id = %s AND folder_name = %s",
            (self.user_id, self.folder_name),
        )
        conn.commit()
        conn.close()

    def get_passwords(self) -> list[Password]:
        """
        Get all the passwords associated with this folder

            Parameters:
                self: The specific instance of the class

            Returns:
                passwords (Password[]): The desired passwords
        """
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
        # Create an instance of the password class for each password in the folder
        for password_id in password_ids:
            passwords.append(Password(self.user_id, password_id))
        self.passwords = passwords
        return passwords


def create_folder(user_id: str, folder_name: str) -> Folder:
    """
    Creates a new folder

        Parameters:
            user_id (str): The user ID associated with the folder
            folder_name (str): The name of the folder

        Returns:
            folder (Folder): The new folder
    """
    # All folder names should be capitalised
    folder_name = folder_name.capitalize()
    conn, cursor = connect()
    # Check if the folder already exists before creating a new one
    cursor.execute(
        "SELECT * FROM folders WHERE user_id = %s AND folder_name= %s",
        (user_id, folder_name),
    )
    out = cursor.fetchone()
    if out is not None:
        raise FolderAlreadyExistsError()
    # Create the new folder
    cursor.execute("INSERT INTO folders VALUES (%s, %s)", (user_id, folder_name))
    conn.commit()
    conn.close()
    # Return an instance of the folder class
    return Folder(user_id, folder_name)
