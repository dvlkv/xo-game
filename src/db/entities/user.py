from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..base import Base
from utils.dict import pick


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    password_salt = Column(String)

    games = relationship('Game')

    def __repr__(self):
        return "<User(email='%s')>" % (self.email)

    def to_json(self):
        return pick(self.__dict__, ['id', 'name', 'email'])
