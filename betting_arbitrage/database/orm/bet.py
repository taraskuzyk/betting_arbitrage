from datetime import datetime

from sqlalchemy import String, Column, Float, Enum, DateTime, Integer, Date, Text

from database.orm.base import Base
from enums.sport import Sport
from enums.website import Website


class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, nullable=False)

    team_1_name = Column(String(50), nullable=False)
    team_1_odds = Column(Float, nullable=False)

    team_2_name = Column(String(50), nullable=False)
    team_2_odds = Column(Float, nullable=False)

    draw_odds = Column(Float, nullable=True)

    match_datetime = Column(Date)
    tournament_name = Column(Text)

    sport = Column(Enum(Sport), nullable=False)
    website = Column(Enum(Website), nullable=False)

    datetime_scraped = Column(DateTime, nullable=False, default=datetime.now())

