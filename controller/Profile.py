import pandas as pd
from flask import jsonify

from Model import  User


class profile():
#     @staticmethod
#     def get_admin_profiles():
#         admin_profiles = Admin.query.all()
#         result = []
#         for admin_profiles in admin_profiles:
#             result.append({
#                 'id': admin_profiles.id,
#                 'email': admin_profiles.email,
#                 'password': admin_profiles.password,
#                 'username': admin_profiles.username,
#                 # เพิ่มฟิลด์อื่น ๆ ตามต้องการ
#             })
#         return jsonify(result)
#
#     @staticmethod
#     def get_mechanic_profile(mechanic_id):
#         mechanic = Mechanic.query.get(mechanic_id)
#         if mechanic is None:
#             return jsonify({'message': 'Mechanic not found'}), 404
#
#         # Return the mechanic profile as JSON response
#         return jsonify({
#             'id': mechanic.id,
#             'email': mechanic.email,
#             'password': mechanic.password,
#             'username': mechanic.username,
#             # Add other profile details as needed
#         }), 200

    @staticmethod
    def get_user_profile(user_id):
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'message': 'user not found'}), 404

        # Return the mechanic profile as JSON response
        return jsonify({
            'id': user.user_id,
            'email': user.email,
            'password': user.password,
            'username': user.username,
            'phoneNumber': user.phoneNumber,
            # Add other profile details as needed
        }), 200