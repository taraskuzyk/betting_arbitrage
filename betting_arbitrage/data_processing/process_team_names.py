from pprint import pprint

from database import Database, Bet
from database.orm import Base
from definitions import ROOT_DIR
from enums.sport import Sport


def main():
    db = Database(
        url=f"sqlite:///{str(ROOT_DIR / 'betting_odds.db')}",
        metadata=Base.metadata,
    )

    bets = db.query(Bet).where(Bet.sport == Sport.csgo).all()

    for bet in bets:
        bet.team_1_name = process_team_name(bet.team_1_name)
        bet.team_2_name = process_team_name(bet.team_2_name)

    db.commit()


def process_team_name(team_name: str) -> str:
    team_name = team_name.lower()
    team_name = team_name.replace("ex ", "")
    team_name = team_name.replace("ex-", "")
    team_name = team_name.replace("esports", "")
    team_name = team_name.replace("esport", "")
    team_name = team_name.replace("gaming", "")
    team_name = team_name.replace("team", "")
    team_name = team_name.replace("club", "")
    team_name = team_name.replace("clan", "")
    team_name = team_name.replace("ec", "")
    team_name = team_name.replace(".gg", "")
    team_name = team_name.replace(".", "")
    team_name = team_name.strip()
    team_name = replace_with_main_name_if_available(team_name)
    return team_name


typos = {"nip": "ninjas in pyjamas", "losreyes": "los reyes", "ftw": "for the win"}


def replace_with_main_name_if_available(team_name):
    if team_name in typos:
        return typos[team_name]
    return team_name


if __name__ == "__main__":
    main()
