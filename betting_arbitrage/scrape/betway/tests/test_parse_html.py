from datetime import datetime

import pytest

from definitions import ROOT_DIR
from scrape.betway.parse_html import get_tournaments, get_tournament_name, get_tournament_dates, \
    get_tournament_date_str, get_events_on_date, get_teams_in_event, get_odds_in_event, get_event_time
from scrape.date_funcs import get_datetime_from_date_str_and_time_str

HTML_PATH = ROOT_DIR / "scrape" / "betway" / "tests" / "betway_csgo.html"
with open(str(HTML_PATH), encoding="utf-8") as file:
    HTML = file.read()


@pytest.fixture
def tournament():
    tournaments = get_tournaments(HTML)
    return tournaments[0]


@pytest.fixture
def tournament_date(tournament):
    dates = get_tournament_dates(tournament)
    return dates[0]


@pytest.fixture
def event(tournament_date):
    events = get_events_on_date(tournament_date)
    return events[0]


def test_get_tournaments():
    events = get_tournaments(HTML)
    # for event in events:
    #     print(event.text)
    assert len(events) == 10


def test_get_tournament_name(tournament):
    assert get_tournament_name(tournament) == "BLAST Premier Spring Groups"


def test_get_tournament_events(tournament):
    assert len(get_tournament_dates(tournament)) == 3


def test_get_date_str(tournament_date):
    assert get_tournament_date_str(tournament_date) == 'Fri 28 Jan'


def test_get_events_on_date(tournament_date):
    assert len(get_events_on_date(tournament_date)) == 1


def test_get_teams_in_event(event):
    assert get_teams_in_event(event) == ["NIP", "BIG"]


def test_get_odds_in_event(event):
    assert get_odds_in_event(event) == [1.50, 2.40]


def test_get_event_time(event):
    assert get_event_time(event) == '08:00'


def test_get_datetime_from_date_str_and_event_time():
    datetime_created = get_datetime_from_date_str_and_time_str("Fri 28 Jan", "08:00")
    assert datetime_created == datetime(year=2022, month=1, day=28, hour=8, minute=0)
