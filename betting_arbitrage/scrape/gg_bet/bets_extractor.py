from database.orm.sport import Sport
from database.orm.website import Website
from scrape.gg_bet.parse_html import get_events
from scrape.gg_bet.parse_html import (
    get_tournament_name,
    is_tournament_name_present,
    is_event_live,
    get_odds,
    get_team_names,
    get_event_datetime,
)
from scrape.shared import Bet


class BetsExtractor:
    def __init__(self, sport: Sport):
        self.sport = sport
        self.website = Website.gg_bet

    def extract_bets_from_page(self, html):
        events = get_events(html)
        tournament_vs_events = self.get_tournament_vs_events(events)
        bets = []
        for tournament, events in tournament_vs_events.items():
            for event in events:
                odds = get_odds(event)
                team_names = get_team_names(event)
                event_datetime = get_event_datetime(event)
                bets.append(self.get_bet(odds, team_names, event_datetime, tournament))

        return bets

    @staticmethod
    def get_tournament_vs_events(events):
        tournament_vs_events = {}
        tournament_name = get_tournament_name(events[0])
        for event in events:
            if is_tournament_name_present(event):
                tournament_name = get_tournament_name(event)
                if tournament_name not in tournament_vs_events:
                    tournament_vs_events[tournament_name] = []
            if is_event_live(event):
                tournament_vs_events[tournament_name].append(event)
        return tournament_vs_events

    def get_bet(self, odds_list, team_names, event_datetime, tournament_name):
        return Bet(
            team_1_name=team_names[0],
            team_2_name=team_names[1],
            team_1_odds=odds_list[0],
            team_2_odds=odds_list[1],
            match_datetime=event_datetime,
            sport=self.sport,
            website=self.website,
            tournament_name=tournament_name,
        )
