# This file is used for the production version of the program, for hosting on a server using gunicorn
from app import app

if __name__ == "__main__":
    app.run()
