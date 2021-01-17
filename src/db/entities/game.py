from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import NamedTuple
import uuid
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

    ended = Column(Boolean)
    field = Column(ARRAY(Integer))
    next_seq = Column(Integer)

    moves = relationship('GameMove')

    def field_size(self) -> GameField:
        return GameField(self.width, self.height)

    def __repr__(self):
        return "<Game (width='%s', height='%s')>" % self.field_size()


class GameMove(Base):
    __tablename__ = 'game_moves'
    __table_args__ = (
        UniqueConstraint('game_id', 'seq'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    seq = Column(Integer)

    uid = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)


