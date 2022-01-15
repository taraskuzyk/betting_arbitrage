from datetime import datetime

from sqlalchemy import String, Column, Float, Enum, DateTime, Integer, Date

from database.orm.base import Base
from database.orm.sport import Sport
from database.orm.website import Website


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, nullable=False)

    team_1_name = Column(String(50), nullable=False)
    team_1_odds = Column(Float, nullable=False)

    team_2_name = Column(String(50), nullable=False)
    team_2_odds = Column(Float, nullable=False)

    draw_odds = Column(Float, nullable=True)

    match_date = Column(Date)

    sport = Column(Enum(Sport), nullable=False)
    website = Column(Enum(Website), nullable=False)

    datetime_scraped = Column(DateTime, nullable=False, default=datetime.now())

