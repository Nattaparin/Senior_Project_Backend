from .database import db


class Token(db.Model):
    __tablename__ = 'token'
    Token_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Token = db.Column(db.String(255), unique=True)


    def __init__(self, Token):
        self.Token = Token

    @property
    def serialize(self):
        return {
            'id': self.id,
            'Token': self.Token,
        }

    @staticmethod
    def read_list(list):
        return [m.serialize for m in list]