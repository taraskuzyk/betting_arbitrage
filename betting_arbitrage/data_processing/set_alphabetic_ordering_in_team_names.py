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
        if bet.team_2_name < bet.team_1_name:
            swap_team_places(bet)
            db.commit()

    db.commit()


def swap_team_places(bet):
    team_1_name = bet.team_1_name
    team_2_name = bet.team_2_name
    team_1_odds = bet.team_1_odds
    team_2_odds = bet.team_2_odds
    bet.team_1_name = team_2_name
    bet.team_2_name = team_1_name
    bet.team_1_odds = team_2_odds
    bet.team_2_odds = team_1_odds


if __name__ == "__main__":
    main()