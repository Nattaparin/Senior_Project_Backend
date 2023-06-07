from getpass import getpass

from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from PRO_BACK.model.admin import db_connection

db = SQLAlchemy()

class mecController:
    @staticmethod
    def login():
        # data = request.get_json()
        # email = data['email']
        # password = data['password']
        email = input("Enter your email: ")
        password = getpass("Enter your password: ")

        # Create a cursor object to interact with the database
        cursor = db_connection.cursor()

        # Execute the query to check if the user exists
        cursor.execute("SELECT * FROM pro.mechanic WHERE email=%s AND password=%s", (email, password))

        # Fetch the results
        result = cursor.fetchone()
        cursor.close()
        db_connection.close()

        if result:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid username or password'})

        # Check if a matching record was found
        # if result:
        #     print("Login successful!")
        # else:
        #     print("Invalid username or password!")





if __name__ == "__main__":
    mecController.login()
