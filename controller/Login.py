from flask_sqlalchemy import SQLAlchemy
import jwt
from flask import request, jsonify
import bcrypt

from Model import  User
import datetime

db = SQLAlchemy()


class login:
    @staticmethod
    def login():
        try:
            email = request.get_json()['email']
            password = request.get_json()['password']
            try:
                user = User.query.filter_by(email=email).first()

                if user and password.encode('utf-8') == bytes(user.password, 'utf-8'):
                    print(user)
                    user_data = {
                        'id': user.id,
                        'email': user.email,
                        'password': user.password,
                        'username': user.username,
                        'phoneNumber': user.phoneNumber,
                        'Token_user': user.Token,
                        'role': user.role,
                        # Add any other user data you want to include in the JWT payload
                    }
                    token = jwt.encode(
                        {'user': user_data, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                        'Bearer')
                    role = user.role
                    print(role)
                    return jsonify({'role': role, 'user': user_data, 'token': token}), 200

                else:
                    return jsonify({'message': 'ขออภัย อีเมล หรือ รหัสผ่านของท่านผิด'}), 401

            except:
                return jsonify({'message': 'ขออภัย อีเมล หรือ รหัสผ่านของท่านผิด'}), 401

        except Exception as e:
            print("Exception:", e)
            return jsonify({'message': 'An error occurred during login'}), 500