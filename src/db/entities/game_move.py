from sqlalchemy import *
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base


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