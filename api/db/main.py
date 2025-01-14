import os
import psycopg2
from dotenv import load_dotenv


def connect():
    load_dotenv()
    connection_string = os.getenv("CONNECTION_STRING")
    with psycopg2.connect(connection_string) as conn:
        return conn, conn.cursor()


def create_tables(cursor):
    """
    Creates the tables in the database
    Parameters:
        cursor: The psycopg2 cursor
    """
    tables = (
        """
    CREATE TABLE IF NOT EXISTS users (
        PRIMARY KEY (user_id),
        user_id TEXT NOT NULL,
        email_address TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        password_salt TEXT NOT NULL,
        tfa_enabled BOOLEAN NOT NULL,
        TOTP_secret TEXT
    )""",
        """
    CREATE TABLE IF NOT EXISTS recovery_codes (
        PRIMARY KEY (user_id, code_id),
        user_id TEXT NOT NULL,
        code_id TEXT NOT NULL,
        hashed_code TEXT NOT NULL,
        salt TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )""",
        """
    CREATE TABLE IF NOT EXISTS folders (
        PRIMARY KEY(user_id, folder_name),
        user_id TEXT NOT NULL,
        folder_name TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""",
        """
    CREATE TABLE IF NOT EXISTS passwords (
        PRIMARY KEY(user_id, password_id),
        user_id TEXT NOT NULL,
        password_id TEXT NOT NULL,
        encrypted_password TEXT NOT NULL,
        salt TEXT NOT NULL,
        iv TEXT NOT NULL,
        folder_name TEXT,
        TOTP_secret TEXT,
        website TEXT,
        name TEXT NOT NULL,
        FOREIGN KEY(user_id, folder_name) REFERENCES folders(user_id, folder_name),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""",
        """
    CREATE TABLE IF NOT EXISTS secure_notes (
        PRIMARY KEY(user_id, note_id),
        user_id TEXT NOT NULL,
        note_id TEXT NOT NULL,
        encrypted_data TEXT NOT NULL,
        salt TEXT NOT NULL,
        iv TEXT NOT NULL,
        folder_name TEXT,
        name TEXT NOT NULL,
        FOREIGN KEY(user_id, folder_name) REFERENCES folders(user_id, folder_name),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )
    """,
    )
    for command in tables:
        cursor.execute(command)


if __name__ == "__main__":
    conn, cursor = connect()
    create_tables(cursor)
    conn.commit()
    conn.close()
