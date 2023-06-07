from getpass import getpass

from flask_sqlalchemy import SQLAlchemy
# import jwt
# from flask import request, jsonify
# import bcrypt
# from model.user import user
# import datetime
from PRO_BACK.model.user import db_connection

db = SQLAlchemy()


class UserController:
    @staticmethod
    def login():
        username = input("Enter your username: ")
        password = getpass("Enter your password: ")

        # Create a cursor object to interact with the database
        cursor = db_connection.cursor()

        # Execute the query to check if the user exists
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))

        # Fetch the results
        result = cursor.fetchone()

        # Check if a matching record was found
        if result:
            print("Login successful!")
        else:
            print("Invalid username or password!")

        # Close the cursor and database connection
        cursor.close()
        db_connection.close()


if __name__ == "__main__":
    login()
