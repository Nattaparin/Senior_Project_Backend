from .database import db


class Case(db.Model):
    __tablename__ = 'case'
    case_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Owner_name = db.Column(db.String(255), unique=True)
    car_Model = db.Column(db.String(255))
    LICENSE_PLATE_NUMBER = db.Column(db.String(255), unique=True)
    phoneNumber = db.Column(db.String(10), unique=True)
    car_symptoms = db.Column(db.String(500),)
    date = db.Column(db.String(500),)
    Part_type = db.Column(db.String(255), )
    Car_part = db.Column(db.String(255), )
    car_detail = db.Column(db.String(255), )
    Mec_name = db.Column(db.String(255),)
    car_progress = db.Column(db.String(255),)


    def __init__(self, Owner_name, car_Model, LICENSE_PLATE_NUMBER , phoneNumber, car_symptoms,date,Part_type,Car_part,car_detail,Mec_name,car_progress):
        self.Owner_name = Owner_name
        self.car_Model = car_Model
        self.LICENSE_PLATE_NUMBER = LICENSE_PLATE_NUMBER
        self.phoneNumber = phoneNumber
        self.car_symptoms = car_symptoms
        self.date = date
        self.Part_type = Part_type
        self.Car_part = Car_part
        self.car_detail = car_detail
        self.Mec_name = Mec_name
        self.car_progress = car_progress
    @property
    def serialize(self):
        return {
            'Owner_name': self.Owner_name,
            'car_Model': self.car_Model,
            'LICENSE_PLATE_NUMBER': self.LICENSE_PLATE_NUMBER,
            'phoneNumber': self.phoneNumber,
            'car_detail': self.car_detail,
            'Mec_name': self.Mec_name,
            'Part_type': self.Part_type,
            'Car_part': self.Car_part,
            'car_symptoms': self.car_symptoms,
            'date': self.date,
            'car_progress': self.car_progress
        }

    def to_dict(self):
        return {
            'Owner_name': self.Owner_name,
            'car_Model': self.car_Model,
            'LICENSE_PLATE_NUMBER': self.LICENSE_PLATE_NUMBER,
            'phoneNumber': self.phoneNumber,
            'car_detail': self.car_detail,
            'car_symptoms': self.car_symptoms,
            'date': self.date,
            'Part_type': self.Part_type,
            'Car_part': self.Car_part,
            'Mec_name': self.Mec_name,
            'car_progress': self.car_progress  # If car_progress is a field in your model
        }
    @staticmethod
    def read_list(list):
        return [m.serialize for m in list]