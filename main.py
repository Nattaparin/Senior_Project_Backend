
import json
import secrets

import jwt

from flask import Flask, session
from flask_cors import CORS
from flask_mail import Mail, Message

from sqlalchemy_utils.functions import database_exists, create_database

from Model import Tracking, Case
# from Model import Case
from Model.UserType import UserRole
from Model.database import db
from Model.model import NeuralNet
from Model.user import User
# from flask import request, jsonify
import datetime
# from src.nltk_utils import bag_of_words, tokenize
# import pythainlp
import torch
from controller import ReceiveCase, Login, Profile, chat
from controller.CaseDetail import CaseDetail
# from controller.CaseDetail import CaseDetail
from controller.Profile import profile
from controller.Register import Register

from controller.case import case

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@127.0.0.1:3306/pro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if not database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    create_database(app.config["SQLALCHEMY_DATABASE_URI"])

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'nattaparin455@gmail.com'
app.config['MAIL_PASSWORD'] = 'mrlmboldbheyxjaz'
app.config['MAIL_DEFAULT_SENDER'] = ('ChatGPT-Engaging-Garage', 'nattaparin455@gmail.com')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('C:/Users/ASUS TUF FA506/OneDrive/เดสก์ท็อป/project/Senior_Project_Backend/src/intents.json', 'r') as json_data:
    intents = json.load(json_data)

mail = Mail(app)
db.init_app(app)

with app.app_context():
    db.create_all()


sounds_data = {
    'ชิ้นส่วนบอดี้': ['ฝากระโปรง','กันชนหน้า', 'กระจังหน้า', 'กันชนหลัง','แก้มหน้าซ้าย','แก้มหน้าขวา','แก้มหลังซ้าย','แก้มหลังขวา'
                ,'บังโคลนล้อ','แผ่นปิดใต้ห้องเครื่อง','สปอยเลอร์หลัง','ล้อ','ฝาครอบดุมล้อ','ยาง','กระโปรงหลัง','กระจกบานหน้า'
                ,'กระจกบานหลัง','กระจกมองข้าง','ซันรูฟ','น็อตล้อ','โคมไฟหน้า','โคมไฟหลัง','ถังน้ำมัน','ท่อ','ชุดปัดน้ำฝน'],
    'ช่วงล่าง': ['แพล่าง','กันโคลงหน้า','แร็คพวงมาลัย''ปีกนกซ้าย','ปีกนกขวา','บูส','ลูกหมากกันโครง','ลูกหมากแร็ค','ลูกหมากปีกนก'
                ,'แท่นเครื่อง','แท่นเกียร์','เบ้ารองโซ็ค','จานเบรก','คาลิปเปอร์เบรก','ผ้าเบรก','สายน้ำมันเบรก','เพลากลาง''เพลาหน้า'
                ,'โซ๊ค'],''
    'อุปกรณ์ภายในห้องเครื่อง': ['เครื่องยนต์','เกียร์','หัวฉีด','หัวเทียน','คอยล์','แบตเตอรี่','เซนเซอร์ต่างๆ','ฟิวส์','กล่องฟิวส์','ECU','รางหัวฉีด'
                ,'หม้อน้ำ','ถังพักน้ำ','หม้อลม','กระปุกน้ำมันเบรก''สายคันเร่ง','ท่อน้ำ','อินเตอร์','เทอร์โบ','คอไอดี','แฮดเดอร์'
                ,'สายพานหน้าเครื่อง','ท่อน้ำ','หน้าปัดไมล์'],
    'ภายใน': ['คอนโซนกลาง', 'คอนโซนหน้า', 'ดีเลย์เสีย','วิทยุ','เบาะหน้า','เบาะหลัง','พรมเหยียบ','พรมพื้นรถ','ชุดแป้นเหยียบ'
                ,'หัวเกียร์','แท่นเกียร์','แผงประตู','กลอนประตู','กระจกมองหลัง'],
    'ของเหลว': ['น้ำมันเครื่อง', 'น้ำมันเกียร์', 'น้ำยาหล่อเย็น', 'น้ำมันเบรก'],

}

# ข้อมูลอาการของรถแต่ละล้อ
problems_data = {
    'ชิ้นส่วนบอดี้': ['ชิ้นส่วนบอดี้'],
    'ช่วงล่าง': ['ช่วงล่าง'],
    'อุปกรณ์ภายในห้องเครื่อง': ['อุปกรณ์ภายในห้องเครื่อง'],
    'ภายใน': ['ภายใน'],
    'ของเหลว': ['ของเหลว'],
}
@app.route('/sounds/<option>')
def get_sounds(option):
    return jsonify(sounds_data.get(option, []))

@app.route('/problems/<option>')
def get_problems(option):
    return jsonify(problems_data.get(option, []))


# @app.route('/login', methods=['POST'])
# def login():
#     return Login.login.login()
@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.get_json()['email']
        password = request.get_json()['password']
        try:
            user = User.query.filter_by(email=email).first()
            if user and password.encode('utf-8') == bytes(user.password, 'utf-8') and user.role == 'admin':
                print(user)
                user_data = {
                    'id': user.user_id,
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
            if user and password.encode('utf-8') == bytes(user.password, 'utf-8') and user.role == 'mechanic':
                print(user)
                user_data = {
                    'id': user.user_id,
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
            if user and password.encode('utf-8') == bytes(user.password, 'utf-8') and user.role == 'user':
                print(user)
                user_data = {
                    'id': user.user_id,
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

@app.route('/check_role', methods=['GET'])
def check_role():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'role': None})

    user = User.query.get(user_id)
    return jsonify({'role': user.role})


@app.route('/register   ', methods=['POST'])
def register():
    return Register.register()

# @app.route('/get-roles', methods=['POST'])
# def get_roles():
#     email = request.json.get('email')
#
#     admin = User.query.filter_by(email=email).first()
#     if admin:
#         roles = [role.name for role in admin.roles]
#         return jsonify({'roles': roles}), 200
#
#     return jsonify({'message': 'User not found'}), 404
# @app.route('/get-roles-mec', methods=['POST'])
# def get_roles_mec():
#     email = request.json.get('email')
#
#
#     mec = User.query.filter_by(email=email).first()
#     if mec:
#         roles = [role.name for role in mec.roles]
#         return jsonify({'roles': roles}), 200
#
#     return jsonify({'message': 'User not found'}), 404

@app.route('/get-roles/<int:user_id>', methods=['GET'])
def get_roles_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'role': None}), 404  # Return 404 Not Found if the user doesn't exist

    role = user.role

    user_type = UserRole.query.filter_by(role=role).first()

    if user_type is None:
        return jsonify({'message': 'Invalid user role'}), 400  # Return 400 Bad Request if the user's role is invalid

    role = user_type.role

    return jsonify({'role': role}), 200
@app.route('/get-plates', methods=['GET'])
def get_plates():
    cases = Case.query.all()
    return jsonify([case.LICENSE_PLATE_NUMBER for case in cases])

# @app.route('/admin', methods=['GET'])
# def get_admin_profiles():
#     return profile. get_admin_profiles()
#
# @app.route('/admin/<int:admin_id>', methods=['PUT'])
# def chang_admin_profiles(admin_id):
#     admin = User.query.get(admin_id)
#     data = request.get_json()
#     if not data:
#         return jsonify({'message': 'No input data provided'}), 400
#
#     if 'email' in data:
#         admin.email = data['email']
#     if 'password' in data:
#         admin.password = data['password']
#     if 'username' in data:
#         admin.username = data['username']
#
#     db.session.commit()
#
#     if data.get('username') == admin.username or data.get('email') == admin.email:
#         return jsonify({'message': 'ชื่อ อีเมลหรือเบอร์ถูกใช้งานไปแล้ว'}), 401
#     return jsonify({'message': 'User updated successfully'}), 200
#
#
#
# @app.route('/MechanicPro/<int:mechanic_id>', methods=['GET'])
# def get_mechanic_profile(mechanic_id):
#     return Profile.profile.get_mechanic_profile(mechanic_id)
#
# @app.route('/MechanicUp/<int:mec_id>', methods=['PUT'])
# def chang_mec_profiles(mec_id):
#     mec = User.query.get(mec_id)
#     data = request.get_json()
#     if 'email' in data:
#         mec.email = data['email']
#     if 'password' in data:
#         mec.password = data['password']
#     if 'username' in data:
#         mec.username = data['username']
#
#     db.session.commit()
#     if data.get('username') == mec.username or data.get('email') == mec.email:
#         return jsonify({'message': 'ชื่อหรืออีเมลถูกใช้งานไปแล้ว'}), 401
#     return jsonify({'message': 'User updated successfully'}), 200
@app.route('/UserPro/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    return profile.get_user_profile(user_id)

# @app.route('/userUp/<int:user_id>', methods=['PUT'])
# def change_user_profiles(user_id):
#     user = User.query.get(user_id)
#
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
#
#     data = request.get_json()
#
#     changed = False
#
#     if 'email' in data:
#         user.email = data['email']
#         changed = True
#     if 'password' in data:
#         user.password = data['password']  # replace with your hashing function
#         changed = True
#     if 'username' in data:
#         user.username = data['username']
#         changed = True
#     if 'phoneNumber' in data:
#         user.phoneNumber = data['phoneNumber']
#         changed = True
#
#     if not changed:
#         return jsonify({'message': 'No changes made'}), 200
#
#     db.session.commit()
#     if data is None:
#         return jsonify({'message': 'No data provided'}), 400
#
#     existing_user_email = User.query.filter_by(email=data.get('email')).first()
#     if existing_user_email and existing_user_email.user_id != user.user_id:
#         return jsonify({'message': 'อีเมลนี้ถูกใช้งานไปแล้ว'}), 400
#
#     existing_user_username = User.query.filter_by(username=data.get('username')).first()
#     if existing_user_username and existing_user_username.user_id != user.user_id:
#         return jsonify({'message': 'ชื่อนี้ถูกใช้งานไปแล้ว'}), 400
#
#     existing_user_phone = User.query.filter_by(phoneNumber=data.get('phoneNumber')).first()
#     if existing_user_phone and existing_user_phone.user_id != user.user_id:
#         return jsonify({'message': 'เบอร์ถูกใช้งานไปแล้ว'}), 400
#     return jsonify({'message': 'User updated successfully'}), 200


@app.route('/userUp/<int:id>', methods=['PUT'])
def change_user_profiles(id):
    user = User.query.get(id)
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'username' in data:
        user.username = data['username']
    if 'phoneNumber' in data:
        user.phoneNumber = data['phoneNumber']

    db.session.commit()
    if data.get('email') != user.email:
        return jsonify({'message': 'อีเมลนี้ถูกใช้งานไปแล้ว'}), 400

    if data.get('username') != user.username:
        return jsonify({'message': 'ชื่อนี้ถูกใช้งานไปแล้ว'}), 400

    if data.get('phoneNumber') != user.phoneNumber:
        return jsonify({'message': 'เบอร์ถูกใช้งานไปแล้ว'}), 400
    return jsonify({'message': 'ทำการบันทึกแล้ว'}), 200


@app.route('/Mechanic', methods=['GET'])
def get_technicians():
    role = 'mechanic'
    technicians = User.query.filter_by(role=role).all()

    if not technicians:
        return jsonify({'error': 'No technicians found'}), 404

    # Debugging line
    print([vars(tech) for tech in technicians])

    result = [tech.username for tech in technicians]
    print("Result:", result)  # Debugging line

    return jsonify(result), 200


#
@app.route('/case', methods=['GET'])
def get_case():
    return case.get_case()
#
@app.route('/case/:<id>', methods=['GET'])
def get_caseID(id):
    return CaseDetail.get_caseID(id)
#
#
@app.route('/registerCase', methods=['POST'])
def register_case():
    return ReceiveCase.register_case.register_case()


# import secrets
# @app.route('/token', methods=['GET'])
# def token():
#     from Model.Token import Token
#     Token = Token.query.all()
#     result = []
#     for Token in Token:
#         result.append({
#             'Token': Token.Token
#             # เพิ่มฟิลด์อื่น ๆ ตามต้องการ
#         })
#     return jsonify(result)
# #
# #
# from flask_mail import Mail, Message
import secrets
#
# # Initialize Flask-Mail
#
#
# @app.route('/generate-token/<int:id>', methods=['GET'])
# def generate_token(id):
#     user = User.query.get(id)
#
#     if user is None:
#         return jsonify({'message': 'User not found'}), 404
#
#     max_attempts = 5  # maximum attempts to generate a unique token
#     for _ in range(max_attempts):
#         generated_token = secrets.token_hex(16)
#         existing_user = User.query.filter_by(Token=generated_token).first()
#
#         if existing_user is None:
#             user.Token = generated_token
#             try:
#                 db.session.commit()
#                 return jsonify({'message': 'Token generated successfully', 'token': generated_token}), 200
#             except Exception as e:
#                 return jsonify({'message': 'Error generating token: ' + str(e)}), 500
#
#     return jsonify({'message': 'Failed to generate a unique token after several attempts'}), 500
#
#
def send_token_to_email(email, token):
    if email is None:
        # Handle the case when email is missing for the user
        return jsonify({'message': 'Email address is missing for the user.'}), 400

    msg = Message('ChatGPT-Engaging-Garage ', recipients=[email])
    msg.body = f'Your token is: {token}'
    mail.send(msg)

    return jsonify({'message': 'Token sent successfully to the provided email.'}), 200


@app.route('/send-token', methods=['POST'])
def send_token():
    email = request.json.get('email')

    if not email:
        return jsonify({'message': 'กรุณาเติมช่องว่างให้ครบ'}), 400

    # Fetch the user from the database based on the provided email
    user = User.query.filter_by(email=email).first()

    if user is None:
        # If the user is not found, create a new user with the provided email and a generated token
        generated_token = secrets.token_hex(16)
        save_user = User(email=email, password=None, username=None, phoneNumber=None, role='user',
                         Token=generated_token)
        db.session.add(save_user)
        db.session.commit()

        # Send the token to the user's email
        send_token_to_email(email, generated_token)
        return jsonify({'message': 'Token sent successfully to the provided email.', 'Token': generated_token}), 200
    else:
        # If the user is found, send the token associated with the user
        send_token_to_email(user.email, user.Token)
        return jsonify({'message': 'Token sent successfully to the provided email.','Token': user.Token}), 200

# @app.route('/search', methods=['GET'])
# def search_case():
#     try:
#         search_value = request.args.get('searchValue')
#
#         # Perform the search in the database based on the provided searchValue
#         # Assuming you have a Case model with Mec_name and LICENSE_PLATE_NUMBER fields
#         search_results = Case.query.filter(
#             (Case.Mec_name.ilike(f'%{search_value}%')) |
#             (Case.LICENSE_PLATE_NUMBER.ilike(f'%{search_value}%'))
#         ).all()
#
#         # Convert the search results to a list of dictionaries
#         results_list = []
#         for result in search_results:
#             result_dict = {
#                 'Owner_name': result.Owner_name,
#                 'car_Model': result.car_Model,
#                 'LICENSE_PLATE_NUMBER': result.LICENSE_PLATE_NUMBER,
#                 'phoneNumber': result.phoneNumber,
#                 'car_detail': result.car_symptoms,
#                 'problems': result.problems,
#                 'sounds': result.sounds,
#                 'Mec_name': result.Mec_name
#             }
#             results_list.append(result_dict)
#
#         if not results_list:
#             return jsonify({'message': 'No results found.', 'results': []}), 200
#
#         return jsonify({'results': results_list}), 200
#     except Exception as e:
#         return jsonify({'message': 'An error occurred during the search.'}), 500

# @app.post("/cahtbot")
# def predict():
#     text = request.get_json().get("message")
#     response = get_response(text)
#     message = {"answer": response}
#     return jsonify(message)
chat_history = []

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    return jsonify({'chat_history': chat_history})

from flask import  request, jsonify
user_states = {}  # To keep track of each user's state
brand_prices = {
        'engine_oil_change': [
            ("Liqui Moly 5w-40 4 L", 2000),
            ("Liqui Moly 5w-50 4 L", 2500),
            ("Motul 5w-50 4 L", 2200),
            ("Motul 5w-40 4 L", 1800)
        ],
        'brake_oil_change': [
            ("Bamboo DOT4 1000ml", 450),
            ("Bamboo DOT5.1 1000ml", 550),
            ("Motul DOT 3 500ml", 210),
            ("Motul DOT 4 500ml", 240),
            ("Motul DOT 5.1 500ml", 360)
        ],
        'coolant_change': [
            ("Liqui Moly RAF 12+ 5L", 800),
            ("Bamboo DOT5.1 1000ml", 550)
        ],
        'change_transmission_oil': [
            ("Motul MULTI CVTF 4L", 1300),
            ("Motul ATF VI 4L", 1450),
            ("LIQUI MOLY ATF7 5L", 2000)
        ]
    }
# @app.route('/chatbot1', methods=['POST'])
# def car_issue_solution1():
#     payload = request.get_json()
#     message = payload.get('message')
#     if not message:
#         return jsonify({"error": "Message is missing"}), 400
#     response = chat.get_car_issue_solution(message)
#     return jsonify({"message": response})
# @app.route('/chatbot2', methods=['POST'])
# def chatbot_route():
#     payload = request.get_json()
#     message = payload.get('message')
#     if not message:
#         return jsonify({"error": "Message is missing"}), 400
#     response = chat.chat_with_gpt4(message)
#     return jsonify({"message": response})

@app.route('/chatbot', methods=['POST'])
def car_issue_solution():
    global DISTANCE_LAST, DISTANCE_NOW
    try:
        payload = request.get_json()
        user_id = payload.get('user_id', None)
        user_message = payload.get('message', '')

        if not user_message:
            return jsonify({"error": "Message is missing"}), 4
        # Rest of your code...

        chatbot_response = ''  # Initialize chatbot_response here

        if user_id not in user_states:
            user_states[user_id] = {'stage': 'initial', 'DISTANCE_LAST': None, 'DISTANCE_NOW': None, 'LICENSE_PLATE': None}

        state = user_states[user_id]
        if state['stage'] == 'initial':
            if "ระยะการเปลี่ยนของเหลว" in user_message:
                chatbot_response = 'กรุณาใส่ระยะทางที่เปลี่ยนของเหลวครั้งล่าสุด'
                state['stage'] = 'awaiting_DISTANCE_LAST'
            elif user_message.startswith("ติดตามสถานะของรถ"):
                chatbot_response = 'กรุณาใส่หมายเลขทะเบียนรถ'
                state['stage'] = 'awaiting_LICENSE_PLATE'

        elif state['stage'] == 'awaiting_DISTANCE_LAST':

            try:

                DISTANCE_LAST = int(user_message)

                state['DISTANCE_LAST'] = DISTANCE_LAST

                chatbot_response = 'กรุณาใส่ระยะทางปัจจุบัน'

                state['stage'] = 'awaiting_DISTANCE_NOW'

            except ValueError:

                chatbot_response = 'กรุณาใส่ตัวเลขเท่านั้น'


        elif state['stage'] == 'awaiting_DISTANCE_NOW':

            try:

                DISTANCE_NOW = int(user_message)

                state['DISTANCE_NOW'] = DISTANCE_NOW

                chatbot_response = 'ข้อมูลอ้างอิงมาจากผลิตภัณฑ์ของ Liqui Moly, Motul ที่ใช้กับรถลูกค้าครับ'

                state['stage'] = 'initial'

            except ValueError:

                chatbot_response = 'กรุณาใส่ตัวเลขเท่านั้น'

        elif state['stage'] == 'awaiting_LICENSE_PLATE':
            license_plate_number = user_message
            state['LICENSE_PLATE'] = license_plate_number
            print(state['LICENSE_PLATE'])
            case_data = Case.query.filter_by(LICENSE_PLATE_NUMBER=license_plate_number).first()
            print(case_data)
            if case_data:
                chatbot_response = f"สถานะ: {case_data.car_progress}"  # assuming case_data has a status attribute
            else:
                chatbot_response = "ไม่พบข้อมูลสำหรับทะเบียนรถนี้"
            state['stage'] = 'initial'
        if "ระยะการเปลี่ยนถ่ายของน้ำมันเครื่อง" in user_message:
            DISTANCE_LAST = state.get('DISTANCE_LAST')
            DISTANCE_NOW = state.get('DISTANCE_NOW')
            if DISTANCE_LAST is not None and DISTANCE_NOW is not None:
                distance_left = 10000 - (DISTANCE_NOW - DISTANCE_LAST)
                if distance_left >= 500:
                    products = "\n".join([f"{brand}: {price}" for brand, price in brand_prices['engine_oil_change']])
                    chatbot_response = f"เหลือระยะทางอีก: {distance_left}\nควรทำการเปลี่ยนถ่ายน้ำมันเครื่องได้แล้ว\nBrand:\n{products}\nต้องการสอบถามเพิ่มเติมสมารถเข้ามาสอบถามหน้าอู่ได้เลยครับ"
                else:
                    chatbot_response = f"เหลือระยะทางอีก: {distance_left} ยังใช้ต่อไปได้"
        if "ระยะการเปลี่ยนถ่ายของนํ้ามันเบรค" in user_message:
            DISTANCE_LAST = state.get('DISTANCE_LAST')
            DISTANCE_NOW = state.get('DISTANCE_NOW')
            if DISTANCE_LAST is not None and DISTANCE_NOW is not None:
                distance_left = 10000 - (DISTANCE_NOW - DISTANCE_LAST)
                if distance_left >= 500:
                    products = "\n".join([f"{brand}: {price}" for brand, price in brand_prices['engine_oil_change']])
                    chatbot_response = f"เหลือระยะทางอีก: {distance_left}\nควรทำการเปลี่ยนถ่ายน้ำมันเครื่องได้แล้ว\nBrand:\n{products}\nต้องการสอบถามเพิ่มเติมสมารถเข้ามาสอบถามหน้าอู่ได้เลยครับ"
                else:
                    chatbot_response = f"เหลือระยะทางอีก: {distance_left} ยังใช้ต่อไปได้"
        elif state['stage'] == 'initial':
            if "ระยะการเปลี่ยนถ่ายของนํ้ามันเกียร์" in user_message:
                DISTANCE_LAST = state.get('DISTANCE_LAST')
                DISTANCE_NOW = state.get('DISTANCE_NOW')
                if DISTANCE_LAST is not None and DISTANCE_NOW is not None:
                    distance_left = 100000 - (DISTANCE_NOW - DISTANCE_LAST)
                    if distance_left >= 500:
                        products = "\n".join(
                            [f"{brand}: {price}" for brand, price in brand_prices['coolant_change']])
                        chatbot_response = f"เหลือระยะทางอีก: {distance_left}\nควรทำการเปลี่ยนถ่ายน้ำมันเครื่องได้แล้ว\nBrand:\n{products}\nต้องการสอบถามเพิ่มเติมสมารถเข้ามาสอบถามหน้าอู่ได้เลยครับ"
        elif state['stage'] == 'initial':
            if "ระยะการเปลี่ยนถ่ายของนํ้ายาหม้อนํ้าหรือนํ้าหล่อเย็น" in user_message:
                DISTANCE_LAST = state.get('DISTANCE_LAST')
                DISTANCE_NOW = state.get('DISTANCE_NOW')
                if DISTANCE_LAST is not None and DISTANCE_NOW is not None:
                    distance_left = 100000 - (DISTANCE_NOW - DISTANCE_LAST)
                    if distance_left >= 500:
                        products = "\n".join(
                            [f"{brand}: {price}" for brand, price in brand_prices['coolant_change']])
                        chatbot_response = f"เหลือระยะทางอีก: {distance_left}\nควรทำการเปลี่ยนถ่ายน้ำมันเครื่องได้แล้ว\nBrand:\n{products}\nต้องการสอบถามเพิ่มเติมสมารถเข้ามาสอบถามหน้าอู่ได้เลยครับ"

        elif state['stage'] == 'initial':
            if "ระยะการเปลี่ยนถ่ายของนํ้ามันเครื่อง" in user_message:
                DISTANCE_LAST = state.get('DISTANCE_LAST')
                DISTANCE_NOW = state.get('DISTANCE_NOW')
                if DISTANCE_LAST is not None and DISTANCE_NOW is not None:
                    distance_left = 10000 - (DISTANCE_NOW - DISTANCE_LAST)
                    if distance_left >= 500:
                        products = "\n".join(
                            [f"{brand}: {price}" for brand, price in brand_prices['brake_oil_change']])
                        chatbot_response = f"เหลือระยะทางอีก: {distance_left}\nควรทำการเปลี่ยนถ่ายน้ำมันเครื่องได้แล้ว\nBrand:\n{products}\nต้องการสอบถามเพิ่มเติมสมารถเข้ามาสอบถามหน้าอู่ได้เลยครับ"
                        showOptions = True

        if not chatbot_response:
            chatbot_response = chat.get_car_issue_solution(user_message)
            state['stage'] = 'initial'
            if chatbot_response.startswith("ขอภัย"):  # If `get_car_issue_solution` cannot provide an answer
                chatbot_response = chat.chat_with_gpt4(user_message)
                state['stage'] = 'initial'
                return jsonify({"message": chatbot_response})
        if chatbot_response:
            # Return the chatbot response as JSON
            return jsonify({"message": chatbot_response})
        if chatbot_response:
            return chatbot_response

        return jsonify({"error": "ขอโทษค่ะ ฉันไม่เข้าใจคำถามของคุณ"})

    except ValueError:
        return jsonify({"error": "กรุณาใส่ตัวเลขเท่านั้น"})


@app.route('/updateCaseStatus', methods=['POST'])
def update_case_status():
    data = request.get_json()
    case_id = data.get('case_id')  # รับ ID ของ Case ที่ต้องการอัพเดต
    print(case_id)
    # ค้นหา Case ด้วย ID
    case_record = Case.query.get(case_id)
    if case_record is None:
        return jsonify({'error': 'Case not found'}), 404

    # ค้นหาสถานะ "อยู่ระหว่างการซ้อม" ในตาราง Tracking
    new_status = Tracking.query.filter_by(Car_progress='อยู่ระหว่างการซ้อม').first()
    if new_status is None:
        return jsonify({'error': 'New status not found in Tracking table'}), 404

    # อัพเดตสถานะ
    case_record.car_progress = new_status.Car_progress
    db.session.commit()

    return jsonify({'message': f'Updated case {case_id} status to อยู่ระหว่างการซ้อม'}), 200

@app.route('/updateCaseStatusRev', methods=['POST'])
def update_case_statusRev():
    data = request.get_json()
    case_id = data.get('case_id')  # รับ ID ของ Case ที่ต้องการอัพเดต

    # ค้นหา Case ด้วย ID
    case_record = Case.query.get(case_id)
    if case_record is None:
        return jsonify({'error': 'Case not found'}), 404

    # ค้นหาสถานะ "อยู่ระหว่างการซ้อม" ในตาราง Tracking
    new_status = Tracking.query.filter_by(Car_progress='ส่งรถเรียบร้อย').first()
    if new_status is None:
        return jsonify({'error': 'New status not found in Tracking table'}), 404

    # อัพเดตสถานะ
    case_record.car_progress = new_status.Car_progress
    db.session.commit()

    return jsonify({'message': f'Updated case {case_id} status to ส่งรถแล้ว'}), 200

@app.route('/get_progrcess', methods=['GET'])
def get_progrcess():
        case_item = Tracking.query.all()
        print(case_item)
        result = []
        for case in case_item:
            result.append({
                'Case_progress_id': case.Case_progress_id,
                'Car_progress': case.Car_progress,
            })
        return jsonify(result)


@app.route('/update_case/<int:case_id>', methods=['PUT'])
def update_case(case_id):
    case = Case.query.get(case_id)
    if not case:
        return jsonify({"message": "Case not found"}), 404

    data = request.json
    if 'Part_type' in data:
        case.Part_type = f"{case.Part_type}, {data['Part_type']}" if case.Part_type else data['Part_type']
    if 'Car_part' in data:
        case.Car_part = f"{case.Car_part}, {data['Car_part']}" if case.Car_part else data['Car_part']
    if 'car_symptoms' in data:
        case.car_symptoms = f"{case.car_symptoms}, {data['car_symptoms']}" if case.car_symptoms else data['car_symptoms']

    db.session.commit()
    return jsonify(case.to_dict()), 200


if __name__ == '__main__':
    app.run(debug=True)

