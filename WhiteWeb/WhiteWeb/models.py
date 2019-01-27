from WhiteWeb import db,app ,login_manager
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

hash=Bcrypt(app)

@login_manager.user_loader
def load_user(userid):
    print(User.query.get(userid))
    return User.query.get(userid)


class User(db.Model,UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    password = db.Column(db.String(30))

    def __init__(self, name=None, password=None, email=None):
        self.name = name
        self.password = password

    def check_password(self, password):
        return hash.check_password_hash(self.password,password)
