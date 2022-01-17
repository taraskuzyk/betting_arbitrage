from datetime import datetime

from database import Database
from enums.sport import Sport
from enums.website import Website
from scrape.db_interface import DBInterface
from scrape.powbet import get_html_from_page
from scrape.powbet.parse_html import (
    get_tournaments,
    get_odds_in_event,
    get_teams_in_event,
    get_tournament_name,
    get_event_datetime_str,
    get_events,
)
from scrape.shared import Bet


class BetsExtractor:
    def __init__(self, db: Database, sport: Sport):
        self.sport = sport
        self.website = Website.powbet
        self.db_interface = DBInterface(db)

    def run(self):
        html = get_html_from_page(*SPORT_TO_CATEGORY_SPORT[self.sport])
        bets = self.extract_bets_from_page(html)
        self.db_interface.add_bets_to_db(bets)

    def extract_bets_from_page(self, html):
        tournaments = get_tournaments(html)
        bets = []
        for tournament in tournaments:
            bets.extend(self.get_bets_from_tournament(tournament))
        return bets

    def get_bets_from_tournament(self, tournament):
        tournament_name = get_tournament_name(tournament)
        events = get_events(tournament)
        bets = []
        for event in events:
            if "live" in event.text.lower():
                continue
            odds_list = get_odds_in_event(event)
            team_names = get_teams_in_event(event)
            event_time = datetime.strptime(
                get_event_datetime_str(event) + " " + str(datetime.now().year),
                "%d/%m %H:%M %Y",
            )
            bets.append(
                self.get_bet(odds_list, team_names, event_time, tournament_name)
            )
        return bets

    def get_bet(self, odds_list, team_names, event_time, tournament_name):
        return Bet(
            team_1_name=team_names[0],
            team_2_name=team_names[1],
            team_1_odds=odds_list[0],
            team_2_odds=odds_list[1],
            match_datetime=event_time,
            sport=self.sport,
            website=self.website,
            tournament_name=tournament_name,
        )


SPORT_TO_CATEGORY_SPORT = {
    Sport.csgo: ("E-sports +", "Counter-Strike: Global Offensive")
}