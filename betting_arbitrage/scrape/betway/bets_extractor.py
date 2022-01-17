from database import Database
from enums.sport import Sport
from enums.website import Website
from scrape.betway import get_html_from_page
from scrape.betway.parse_html import (
    get_tournaments,
    get_tournament_dates,
    get_tournament_date_str,
    get_events_on_date,
    get_odds_in_event,
    get_teams_in_event,
    get_event_time,
    get_tournament_name,
)
from scrape.date_funcs import get_datetime_from_date_str_and_time_str
from scrape.db_interface import DBInterface
from scrape.shared import Bet


class BetsExtractor:
    def __init__(self, db: Database, sport: Sport):
        self.sport = sport
        self.website = Website.betway
        self.db_interface = DBInterface(db)

    def run(self):
        html = get_html_from_page(SPORT_TO_URL[self.sport])
        bets = self.extract_bets_from_page(html)
        self.db_interface.add_bets_to_db(bets)

    def extract_bets_from_page(self, html):
        tournaments = get_tournaments(html)
        bets = []
        for tournament in tournaments:
            bets.extend(self.get_bets_from_tournament(tournament))
        return bets

    def get_bets_from_tournament(self, tournament):
        dates = get_tournament_dates(tournament)
        bets = []
        for date in dates:
            bets.extend(self.get_bets_from_date(date))
        for bet in bets:
            bet.tournament_name = get_tournament_name(tournament)
        return bets

    def get_bets_from_date(self, date):
        date_str = get_tournament_date_str(date)
        events = get_events_on_date(date)
        bets = []
        for event in events:
            odds_list = get_odds_in_event(event)
            team_names = get_teams_in_event(event)
            event_time = get_event_time(event)
            bets.append(self.get_bet(odds_list, team_names, event_time, date_str))
        return bets

    def get_bet(self, odds_list, team_names, event_time, date_str):
        return Bet(
            team_1_name=team_names[0],
            team_2_name=team_names[1],
            team_1_odds=odds_list[0],
            team_2_odds=odds_list[1],
            match_datetime=get_datetime_from_date_str_and_time_str(
                date_str, time_str=event_time
            ),
            sport=self.sport,
            website=self.website,
        )


SPORT_TO_URL = {Sport.csgo: "https://betway.com/en/sports/sct/esports/cs-go"}