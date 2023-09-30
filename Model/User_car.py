
from .database import db

class User_car(db.Model):
    __tablename__ = 'user_car'
    user_car_id = db.Column(db.Integer, primary_key=True)
    Car_model = db.Column(db.String(255))
    License_plate_number = db.Column(db.String(255))

    def __init__(self, Car_model, License_plate_number):
        self.Car_model = Car_model
        self.License_plate_number = License_plate_number

    @property
    def serialize(self):
        return {
            'id': self.id,
            'Car_model':  self.Car_model,
            'License_plate_number': self.License_plate_number,
        }

    @staticmethod
    def read_list(list):
        return [m.serialize for m in list]