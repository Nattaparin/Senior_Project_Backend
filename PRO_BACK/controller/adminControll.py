from getpass import getpass

from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from PRO_BACK.model.admin import db_connection

db = SQLAlchemy()

class adminController:
    @staticmethod
    def login():
        data = request.get_json()
        email = data['email']
        password = data['password']

        # Create a cursor object to interact with the database
        cursor = db_connection.cursor()

        # Execute the query to check if the user exists
        cursor.execute("SELECT * FROM pro.admin WHERE email=%s AND password=%s", (email, password))

        # Fetch the results
        result = cursor.fetchone()
        cursor.close()
        db_connection.close()

        # Check if a matching record was found
        if result:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid username or password'})
        # Close the cursor and database connection



# if __name__ == "__main__":
#     adminController.login()
