
from .database import db

class UserRole(db.Model):
    __tablename__ = 'user_type'
    user_type_id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))

    def __init__(self, role):
        self.role = role

    @property
    def serialize(self):
        return {
            'id': self.id,
            'role':  self.role,
        }

    @staticmethod
    def read_list(list):
        return [m.serialize for m in list]