from .database import db
from .Receive_Case import Case

class Tracking(db.Model):
    __tablename__ = 'Case_progress'
    Case_progress_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Car_progress = db.Column(db.String(255), unique=True)


    def __init__(self, Car_progress):
        self.Car_progress = Car_progress

    @property
    def serialize(self):
        return {
            'id': self.id,
            'Car_progress': self.Car_progress
        }

    @staticmethod
    def read_list(list):
        return [m.serialize for m in list]