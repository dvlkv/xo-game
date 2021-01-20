from sqlalchemy import *
from sqlalchemy.orm import relationship
from typing import NamedTuple
from ..base import Base


class GameField(NamedTuple):
    width: int
    height: int


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)

    uid = Column(Integer, ForeignKey('users.id'))
    width = Column(Integer)
    height = Column(Integer)

    started_at = Column(DateTime)
    ended = Column(Boolean)
    won = Column(Boolean)

    field = Column(ARRAY(Integer))
    next_seq = Column(Integer)

    moves = relationship('GameMove')

    def field_size(self) -> GameField:
        return GameField(self.width, self.height)

    def __repr__(self):
        return "<Game (width='%s', height='%s')>" % self.field_size()


