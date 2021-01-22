from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relationship

from utils.dict import pick
from ..base import Base


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)

    uid = Column(Integer, ForeignKey('users.id'))
    size = Column(Integer)

    started_at: datetime = Column(DateTime)
    duration = Column(Integer)
    ended = Column(Boolean)
    winner = Column(Integer)

    """Array of numbers width * height (9 <= len <= 144)"""
    field: list[list[int]] = Column(ARRAY(Integer, dimensions=2))
    next_seq = Column(Integer)

    moves = relationship('GameMove')

    """Field item getters/setters"""
    def __getitem__(self, pos: tuple[int, int]):
        x, y = pos
        if x < 0 or x > self.size - 1 or y < 0 or y > self.size - 1:
            raise ValueError("x, y should be greater than 0 and lower than field size")

        """Gets field item by (x, y) params"""
        return self.field[y][x]

    def __setitem__(self, pos: tuple[int, int], value: int):
        x, y = pos
        if x < 0 or x > self.size - 1 or y < 0 or y > self.size - 1:
            raise ValueError("x, y should be greater than 0 and lower than field size")

        self.field[y][x] = value
        self.field = [[self[x, y] for x in range(self.size)] for y in range(self.size)]

    def __repr__(self):
        return "<Game (size='%s')>" % self.size

    def to_json(self):
        res = pick(self.__dict__, ['id', 'uid', 'size', 'ended', 'duration', 'winner', 'next_seq'])
        res['field'] = [[self[x, y] for x in range(self.size)] for y in range(self.size)]
        res['started_at'] = round(self.started_at.timestamp())
        if 'moves' not in inspect(self).unloaded:
            res['moves'] = [move.to_json() for move in self.moves]
        return res

