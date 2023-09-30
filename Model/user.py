from .database import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    phoneNumber = db.Column(db.String(10), unique=True)
    Token = db.Column(db.String(255))
    role = db.Column(db.String(20), nullable=False)

    def __init__(self, email, password, username, phoneNumber, Token, role):
        self.email = email
        self.password = password
        self.username = username
        self.phoneNumber = phoneNumber
        self.Token = Token
        self.role = role

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'phoneNumber': self.phoneNumber,
            'Token': self.Token,
            'role': self.role,
        }

    @staticmethod
    def read_list(list):
        return [m.serialize for m in list]
