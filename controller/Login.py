from flask_sqlalchemy import SQLAlchemy
import jwt
from flask import request, jsonify
import bcrypt
from Model.admin import Admin
import datetime

db = SQLAlchemy()


class adminController:
    @staticmethod
    def login():
        try:
            email = request.get_json()['email']
            password = request.get_json()['password']
            try:
                admin = Admin.query.filter_by(email=email).first()
                if bcrypt.checkpw(password.encode('utf-8'), bytes(admin.password, 'utf-8')):
                    admin_serialize = admin.serialize
                    token = jwt.encode(
                        {'admin': admin_serialize, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                        'Bearer')
                    return jsonify({'admin': admin_serialize, 'token': token}), 200
                raise
            except:
                return jsonify({'message': 'username or password is incorrect'}), 401
        except:
            return jsonify({'message': 'The request body required username, password'}), 400