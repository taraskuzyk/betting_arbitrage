from database import Database, Bet
from enums.sport import Sport

"""
        how would I do it by hand:

        1) get a bet
        2) search for bets with this same team name (1st)
        3) select one with matching 2nd team name


        easier way is to create dicts for each bet and compare 
        dicts for reduced search time (around n log n instead of n^2)
"""


class DBInterface:
    def __init__(self, db: Database):
        self.db = db

    def get_list_of_matching_bets(self, sport: Sport):
        bets = self.get_bets_by_sport(sport)
        match_key_vs_bets = {}
        for bet in bets:
            match_key = get_match_key(bet)
            if match_key in match_key_vs_bets:
                match_key_vs_bets[match_key].append(bet)
            else:
                match_key_vs_bets[match_key] = [bet]
        return [bets for _, bets in match_key_vs_bets.items() if len(bets) > 1]

    def get_bets_by_sport(self, sport):
        return self.db.query(Bet).where(Bet.sport == sport).all()


def get_match_key(bet: Bet) -> str:
    return f"{bet.team_1_name} vs {bet.team_2_name}"
