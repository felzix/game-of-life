from hashlib import md5
from sqlalchemy import Column, Integer, String

from game_of_life_web_server import db


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def check_password(self, password_attempt):
        return hash_password(password_attempt) == self.password

    def __repr__(self):
       return "<User(name='%s', password='%s')>" % (self.username, self.password)


def hash_password(password):
    return md5(password).hexdigest()