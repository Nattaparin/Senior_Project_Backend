from .database import db

class Car_Part(db.Model):
    __tablename__ = 'car_part'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body_part = db.Column(db.String(255))
    chassis = db.Column(db.String(255))
    interior_equipment = db.Column(db.String(255))
    interior = db.Column(db.String(255))
    liquid = db.Column(db.String(500))

    def __init__(self, body_part, chassis, interior_equipment, interior, liquid):
        self.body_part = body_part
        self.chassis = chassis
        self.interior_equipment = interior_equipment
        self.interior = interior
        self.liquid = liquid

    @property
    def serialize(self):
        return {
            'id': self.id,
            'body_part': self.body_part,
            'chassis': self.chassis,
            'interior_equipment': self.interior_equipment,
            'interior': self.interior,
            'liquid': self.liquid
        }

    @staticmethod
    def serialize_list(car_parts_list):
        return [car_part.serialize for car_part in car_parts_list]
