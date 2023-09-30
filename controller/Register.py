from flask_sqlalchemy import SQLAlchemy
import jwt
from flask import request, jsonify
import bcrypt

from Model import User, db
# from Model.mechanic import Mechanic
import datetime



class Register:
    @staticmethod
    def register():
        try:
            email = User.email
            password = request.json['password']
            username = request.json['username']
            phoneNumber = request.json['phoneNumber']
            Token_user = request.json['Token']
            role = 'user'  # Set role to 'user'
            user = User.query.filter(User.password.is_(None), User.username.is_(None),
                                     User.phoneNumber.is_(None), ).first()
            existing_user = User.query.filter(
                (User.username == username) | (User.phoneNumber == phoneNumber)
            ).first()
            print(user)
            if existing_user:
                # Return the appropriate message based on which field is already used
                messages = []
                if existing_user.username == username:
                    messages.append('ชื่อนี้ถูกใช้งานไปแล้ว')
                if existing_user.phoneNumber == phoneNumber:
                    messages.append('เบอร์นี้ถูกใช้งานไปแล้ว')
                print(messages)
                return jsonify({'message': ' '.join(messages)}), 401

            # Check if the Token matches with the user's Token
            if Token_user == User.Token:
                save_user = User(email=email, password=password, username=username, phoneNumber=phoneNumber, role=role,
                                 Token=Token_user)
                db.session.add(save_user)

            else:
                user.email = email
                user.password = password
                user.username = username
                user.phoneNumber = phoneNumber
                user.Token_user = Token_user
                user.role = role  # Set role to 'user'

            db.session.commit()
            return jsonify('Pass'), 200
        except Exception as e:
            print(str(e))
            return jsonify({'message': 'Error: ' + str(e)}), 401