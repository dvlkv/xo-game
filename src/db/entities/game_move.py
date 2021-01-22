from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
import uuid

from utils.dict import pick
from ..base import Base


class GameMove(Base):
    __tablename__ = 'game_moves'
    __table_args__ = (
        UniqueConstraint('game_id', 'seq'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    seq = Column(Integer)
    time = Column(DateTime)

    uid = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)

    def to_json(self):
        res = pick(self.__dict__, ['game_id', 'seq', 'uid', 'x', 'y'])
        res['time'] = round(self.time.timestamp())
        res['id'] = str(self.id)
        return res