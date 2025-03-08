import os
import psycopg2
from dotenv import load_dotenv


def connect():
    """
    Connect to the database

        Returns
            conn: The connection to the database
            cursor: The cursor for the database
    """
    load_dotenv()
    host = os.getenv("HOST")
    port = os.getenv("PORT")
    user = os.getenv("USER")
    dbname = os.getenv("DB")
    password = os.getenv("PASSWORD")

    with psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    ) as conn:
        return conn, conn.cursor()


def create_tables(cursor) -> None:
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
        email_verified BOOLEAN NOT NULL,
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
        username TEXT NOT NULL,
        name TEXT NOT NULL,
        folder_name TEXT,
        TOTP_secret TEXT,
        website TEXT,
        FOREIGN KEY(user_id, folder_name) REFERENCES folders(user_id, folder_name),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""",
    )
    for command in tables:
        cursor.execute(command)


if __name__ == "__main__":
    conn, cursor = connect()
    create_tables(cursor)
    conn.commit()
    conn.close()
