from database import Database
from database.orm.base import Base
from database.orm.bet import Bet
from database.orm.website import Website
from definitions import ROOT_DIR

PATH_TO_TEST_DB = ROOT_DIR / "database" / "tests" / "test_betting_odds.db"
TEST_DB_URL = f"sqlite:///{str(PATH_TO_TEST_DB)}"


def test_if_database_gets_created():
    db = Database(url=TEST_DB_URL, metadata=Base.metadata, should_create_schema=True)
    bet = Bet(team_1_name="xd", team_1_odds=1.0, team_2_name="yd", team_2_odds=1, website=Website.luckbox)
    db.add(bet, commit=True)
    assert bet.id == 1
