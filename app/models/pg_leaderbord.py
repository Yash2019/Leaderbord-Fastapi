from app.database.db import Base
from sqlalchemy.orm import Mapped, mapped_column


class LeaderBord(Base):
    __tablename__ = 'leaderbord'
    id: Mapped[int] = mapped_column(primary_key=True)
    game_name: Mapped[str] = mapped_column(nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    player:Mapped[str] = mapped_column(nullable=False) 

