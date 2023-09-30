from .database import db


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)




    def __init__(self, name):
        self.name = name


    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @staticmethod
    def read_list(list):
        return [m.serialize for m in list]