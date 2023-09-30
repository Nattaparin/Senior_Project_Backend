import bcrypt
from sqlalchemy import event

from .Tracking import Tracking
from .Token import Token
from .Receive_Case import Case
from .Car_Part import Car_Part
from .User_car import User_car

# from .Role_user import user_datastore

from .database import db

from .user import User
from .UserType import UserRole

# admin_role = user_datastore.create_role(name='admin', description='Administrator')
# mechanic_role = user_datastore.create_role(name='mechanic', description='Mechanic')
# user_role = user_datastore.create_role(name='user', description='User')
@event.listens_for(UserRole.__table__, 'after_create')
def create_user_roles(*args, **kwargs):
    db.session.add_all([
        UserRole(role='user'),
        UserRole(role='mechanic'),
        UserRole(role='admin')
    ])
    db.session.commit()
@event.listens_for(User_car.__table__, 'after_create')
def create_user_car(*args, **kwargs):
    db.session.add_all([
        User_car(Car_model='Toyota Celica (Gen7)', License_plate_number='จต 2245'),
        User_car(Car_model='BMW F20 M-Sport', License_plate_number=': 2 ขต 6418'),
        User_car(Car_model='Honda Civic FD 2.0', License_plate_number='งว 2804'),
        User_car(Car_model='Toyota Vios 2013 ', License_plate_number='ก 1684'),
        User_car(Car_model='BMW 530i G30 ', License_plate_number='4 ขข 2424'),
        User_car(Car_model='Honda Civic FK 1.5 Turbo ', License_plate_number='กร 8598'),
        User_car(Car_model='Honda Civic ES K24', License_plate_number='กม 2247'),
        User_car(Car_model='Toyota altis 2014', License_plate_number='กก 1111'),
        User_car(Car_model='Honda Civic ES D17', License_plate_number='ฏย 3164'),
        User_car(Car_model='Ford EcoSport 1.5L Ti-VCT', License_plate_number='งพ 7800'),
        User_car(Car_model='Honda Accord G10', License_plate_number='ก 1684'),
        User_car(Car_model='Mercedes-Benz E250 (W212)', License_plate_number='กม 2202'),
        User_car(Car_model='Mazda CX-8 2.2 ', License_plate_number='2 กย 2064'),
        User_car(Car_model='Honda Civic FK 1.5 Turbo ', License_plate_number='กร 8598'),
        User_car(Car_model='Mclaren 720s', License_plate_number='กม 1'),
        User_car(Car_model='Ford Escort MK1 SR20DET', License_plate_number='กญ 166'),
        User_car(Car_model='Honda integra dc2 type r', License_plate_number='กม 2028'),
        User_car(Car_model='Mercedes Benz SL55', License_plate_number='กก 55'),
        User_car(Car_model='Mitsubishi Evolution8 MR', License_plate_number='งง 3333'),
    ])
    db.session.commit()
# @event.listens_for(Admin.__table__, 'after_create')
# def create_user(*args, **kwargs):
#     db.session.add(
#         Admin(email='Tom@hotmail.com', password='123456', username='Tom', role='admin'))
#     db.session.commit()
#
# @event.listens_for(Mechanic.__table__, 'after_create')
# def create_mechanic(*args, **kwargs):
#     db.session.add(
#         Mechanic(email='j@hotmail.com', password='666666', username='jame',role='mechanic'))
#     db.session.add(
#         Mechanic(email='M@hotmail.com', password='999999', username='mark',role='mechanic'))
#     db.session.commit()

@event.listens_for(Case.__table__, 'after_create')
def create_case(*args, **kwargs):
    db.session.add(
        Case(Owner_name='jame', car_Model='Toyota Celica (Gen7)', LICENSE_PLATE_NUMBER='จต 2245',phoneNumber='093333333',car_symptoms='เปลี่ยนถ่ายของเหลว',date='08/01/2014',Part_type='นํ้ามันเครื่อง, นํ้ามันเกียร์, นํ้ายาหล่อเย็น',Car_part='รถมีอาการสะดุด',car_detail='ลูกค้าเข้าเปลี่ยนของเหลวระยะ 100000 km',Mec_name='jame',car_progress='อยู่ระหว่างการซ้อม')),
    db.session.add(
        Case(Owner_name='Pom', car_Model='BMW F20 M-Sport', LICENSE_PLATE_NUMBER='2 ขต 6418', phoneNumber='06345691',car_symptoms='เช็คความพร้อมก่อนขึ้นจูน', date='08/01/2014', Part_type='หัวฉีด,หัวเทียน,คอยล์', Car_part='',
             car_detail='sjnkaj', Mec_name='jame',car_progress='รับรถแล้ว'))
    db.session.commit()
    db.session.add(
        Case(Owner_name='Pon', car_Model='Honda Civic FD 2.0', LICENSE_PLATE_NUMBER='งว 2804', phoneNumber='06355691'
             , car_symptoms='เช็คความพร้อมก่อนขึ้นจูน',
             date='08/01/2014',Part_type='หัวฉีด,หัวเทียน,คอยล์',Car_part='',car_detail='sjnkaj', Mec_name='jame',car_progress='อยู่ระหว่างการซ้อม'))
    db.session.commit()
    db.session.add(
        Case(Owner_name='ice', car_Model='Toyota Vios 2013', LICENSE_PLATE_NUMBER='ก 1684', phoneNumber='06445691', car_symptoms='เช็คความพร้อมก่อนขึ้นจูน',
             date='08/01/2014', Part_type='หัวฉีด,หัวเทียน,คอยล์', Car_part='',
             car_detail='sjnkaj', Mec_name='jame',car_progress='ส่งรถเรียบร้อย'))
    db.session.commit()

@event.listens_for(User.__table__, 'after_create')
def create_user(*args, **kwargs):
    db.session.add(
        User(email='Tom@hotmail.com', password='123456', username='Tom', phoneNumber="083456789", Token='',
             role='admin'))
    db.session.commit()
    db.session.add(
        User(email='j@hotmail.com', password='666666', username='jame', phoneNumber="093456789", Token='',
             role='mechanic'))
    db.session.add(
        User(email='M@hotmail.com', password='999999', username='mark', phoneNumber="063456789", Token='',
             role='mechanic'))
    db.session.add(
        User(email='js@hotmail.com', password='888888', username='jack', phoneNumber="023456789", Token='', role='user')),
    db.session.add(
        User(email='T@hotmail.com', password='777777', username='boom', phoneNumber="123456788", Token='', role='user')),
    db.session.commit()
@event.listens_for(Token.__table__, 'after_create')
def create_token(*args, **kwargs):
    db.session.add(
        Token(Token=''))
    db.session.commit()

@event.listens_for(Tracking.__table__, 'after_create')
def create_token(*args, **kwargs):
    db.session.add(
        Tracking(Car_progress='อยู่ระหว่างการซ้อม'))
    db.session.commit()
    db.session.add(
        Tracking(Car_progress='ส่งรถเรียบร้อย'))
    db.session.commit()
    db.session.add(
        Tracking(Car_progress='รับรถแล้ว'))
    db.session.commit()

@event.listens_for(Car_Part.__table__, 'after_create')
def create_token(*args, **kwargs):
    db.session.add(
            Car_Part(body_part='ฝากระโปรง ', chassis='แพล่าง', interior_equipment='เครื่องยนต์', interior='คอนโซนกลาง', liquid='น้ำมันเครื่อง'))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='กันชนหน้า ', chassis='กันโคลงหน้า', interior_equipment='เกียร์', interior='คอนโซนหน้า', liquid='น้ำมันเกียร์'))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='กระจังหน้า ', chassis='แร็คพวงมาลัย', interior_equipment='หัวฉีด', interior='หน้าปัดไมล์', liquid='น้ำยาหล่อเย็น'))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='กันชนหลัง ', chassis='ปีกนกซ้าย', interior_equipment='หัวเทียน', interior='วิทยุ', liquid='น้ำมันเบรก'))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='แก้มหน้าซ้าย ', chassis='ปีกนกขวา', interior_equipment='คอยล์', interior='เบาะหน้า', liquid=''))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='แก้มหน้าขวา ', chassis='บูส', interior_equipment='แบตเตอรี่', interior='เบาะหลัง', liquid=''))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='แก้มหลังซ้าย ', chassis='ลูกหมากกันโครง', interior_equipment='เซนเซอร์ต่างๆ', interior='พรมเหยียบ', liquid=''))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='ของเหลว ', chassis='ลูกหมากแร็ค', interior_equipment='ฟิวส์', interior='พรมพื้นรถ', liquid=''))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='แก้มหลังขวา ', chassis='ลูกหมากปีกนก', interior_equipment='กล่องฟิวส์', interior='ชุดแป้นเหยียบ', liquid=''))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='บังโคลนล้อ ', chassis='แท่นเครื่อง', interior_equipment='ECU', interior='หัวเกียร์', liquid=''))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='แผ่นปิดใต้ห้องเครื่อง ', chassis='แท่นเกียร์', interior_equipment='รางหัวฉีด', interior='แท่นเกียร์', liquid=''))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='สปอยเลอร์หลัง ', chassis='เบ้ารองโซ็ค', interior_equipment='หม้อน้ำ', interior='แผงประตู', liquid=''))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='ล้อ ', chassis='จานเบรก', interior_equipment='ถังพักน้ำ', interior='กลอนประตู', liquid=''))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='ฝาครอบดุมล้อ ', chassis='คาลิปเปอร์เบรก', interior_equipment='หม้อลม', interior='กระจกมองหลัง', liquid=''))
    db.session.commit()

    db.session.add(
            Car_Part(body_part='ยาง ',chassis='ผ้าเบรก',interior_equipment='กระปุกน้ำมันเบรก',interior=None,liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='กระโปรงหลัง ', chassis='สายน้ำมันเบรก', interior_equipment='สายคันเร่ง', interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='กระจกบานหน้า ', chassis='เพลากลาง', interior_equipment='ท่อน้ำ', interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='กระจกบานหลัง ', chassis='เพลาหน้า', interior_equipment='อินเตอร์', interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='กระจกมองข้าง ', chassis='โซ๊ค', interior_equipment='เทอร์โบ', interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='ซันรูฟ ', chassis=None, interior_equipment='คอไอดี', interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='น็อตล้อ ', chassis=None, interior_equipment='แฮดเดอร์', interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='โคมไฟหน้า ', chassis=None, interior_equipment='สายพานหน้าเครื่อง', interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='โคมไฟหลัง ', chassis=None, interior_equipment='ท่อน้ำ', interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='ถังน้ำมัน ', chassis=None, interior_equipment='สายเกียร์', interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='ท่อ ', chassis=None, interior_equipment=None, interior=None, liquid=None))
    db.session.commit()

    db.session.add(
        Car_Part(body_part='ชุดปัดน้ำฝน ', chassis=None, interior_equipment=None, interior=None, liquid=None))
    db.session.commit()

# @event.listens_for(Case.__table__, 'after_create')
# def create_Role(*args, **kwargs):
#     admin_user = user_datastore.create_user(email='admin@example.com', password='adminpassword')
#     user_datastore.add_role_to_user(admin_user, admin_role)
#
#     mechanic_user = user_datastore.create_user(email='mechanic@example.com', password='mechanicpassword')
#     user_datastore.add_role_to_user(mechanic_user, mechanic_role)
#
#     user = user_datastore.create_user(email='user@example.com', password='userpassword')
#     user_datastore.add_role_to_user(user, user_role)