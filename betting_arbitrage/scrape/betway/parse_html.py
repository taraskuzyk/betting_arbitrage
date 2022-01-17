from bs4 import BeautifulSoup

from scrape.betway.css_strings import TOURNAMENT_SELECTOR


def get_tournaments(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.select(selector=TOURNAMENT_SELECTOR, recursive=False)


def get_tournament_name(tournament_element):
    return tournament_element.select_one(".titleTextWrapper .titleText").text


def get_tournament_dates(tournament_element):
    return tournament_element.select(".collapsablePanel")


def get_tournament_date_str(event_element):
    return event_element.select_one(".titleTextWrapper .titleText").text


def get_events_on_date(date_element):
    return [event for event in date_element.select(".oneLineEventItem") if event.select_one('.score') is None]


def get_teams_in_event(event_element):
    return [team_name.text for team_name in event_element.select(".teamNameFirstPart")]


def get_odds_in_event(event_element):
    return [float(odds.text) for odds in event_element.select(".odds")]


def get_event_time(event_element):
    return event_element.select_one(".oneLineDateTime").text


