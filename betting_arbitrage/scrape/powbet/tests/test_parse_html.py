from datetime import datetime

import pytest

from definitions import ROOT_DIR
from scrape.date_funcs import get_datetime_from_date_str_and_time_str
from scrape.powbet.parse_html import get_tournaments, get_tournament_name, get_events, get_teams_in_event, \
    get_odds_in_event, get_event_datetime_str

HTML_PATH = ROOT_DIR / "scrape" / "powbet" / "tests" / "powbet_csgo.html"
with open(str(HTML_PATH), encoding="utf-8") as file:
    HTML = file.read()


@pytest.fixture
def tournament():
    tournaments = get_tournaments(HTML)
    return tournaments[0]


@pytest.fixture
def event(tournament):
    events = get_events(tournament)
    return events[0]


def test_get_tournaments():
    tournaments = get_tournaments(HTML)
    # for event in events:
    #     print(event.text)
    assert len(tournaments) == 4


def test_get_tournament_name(tournament):
    assert get_tournament_name(tournament) == "Pinnacle Winter Series #1, Counter-Strike: Global Offensive"


def test_get_events(tournament):
    assert len(get_events(tournament)) == 7


def test_get_teams_in_event(event):
    assert get_teams_in_event(event) == ["One Tap Gaming", "Tricked Esport"]


def test_get_odds_in_event(event):
    assert get_odds_in_event(event) == [2.35, 1.52]


def test_get_event_time(event):
    assert get_event_datetime_str(event) == '17/01 01:00'


