from .database import db

class Car_Part(db.Model):
    __tablename__ = 'car_part'
    car_symphoms_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    car_symphoms = db.Column(db.String(255))
    date = db.Column(db.String(255))


    def __init__(self, car_symphoms, date):
        self.date = date
        self.car_symphoms = car_symphoms


    @property
    def serialize(self):
        return {
            'id': self.id,
            'body_part': self.body_part,

        }

    @staticmethod
    def serialize_list(car_parts_list):
        return [car_part.serialize for car_part in car_parts_list]
