import pytest

from arbitrage_finder.db_interface import DBInterface
from database import Database, Bet
from database.orm import Base
from definitions import ROOT_DIR
from enums.sport import Sport
from enums.website import Website


@pytest.fixture(scope="function")
def db():
    return Database(
        url=f"sqlite:///{str(ROOT_DIR / 'arbitrage_finder' / 'test_betting_odds.db')}",
        metadata=Base.metadata,
        should_create_schema=True,
    )


@pytest.fixture(scope="function")
def db_interface(db):
    return DBInterface(db)


def test_find_matching_bets_across_websites(db: Database, db_interface: DBInterface):
    bet_1 = Bet(
        id=1,
        team_1_name="xd",
        team_2_name="lol",
        team_1_odds=1.5,
        team_2_odds=2.5,
        sport=Sport.csgo,
        website=Website.gg_bet,
    )
    bet_2 = Bet(
        id=2,
        team_1_name="xd",
        team_2_name="lol",
        team_1_odds=1.5,
        team_2_odds=2.5,
        sport=Sport.csgo,
        website=Website.powbet,
    )
    bet_3 = Bet(
        id=3,
        team_1_name="not xd",
        team_2_name="lol",
        team_1_odds=1.5,
        team_2_odds=2.5,
        sport=Sport.csgo,
        website=Website.powbet,
    )
    db.add_all([bet_1, bet_2, bet_3], commit=True)

    list_of_matching_bets = db_interface.get_list_of_matching_bets(sport=Sport.csgo)
    assert len(list_of_matching_bets) == 1 and len(list_of_matching_bets[0]) == 2
