import datetime

import pytest

from definitions import ROOT_DIR
from scrape.gg_bet.parse_html import (
    get_events,
    get_non_live_events,
    get_event_datetime,
    get_team_names,
    get_odds, get_tournament_name,
)

HTML_PATH = ROOT_DIR / "scrape" / "gg_bet" / "tests" / "gg_bet_csgo.html"
with open(str(HTML_PATH), encoding="utf-8") as file:
    HTML = file.read()


@pytest.fixture
def event():
    events = get_events(HTML)
    non_live_events = get_non_live_events(events)
    return non_live_events[0]


@pytest.fixture
def event_with_tournament_name():
    events = get_events(HTML)
    non_live_events = get_non_live_events(events)
    return non_live_events[1]


def test_get_events():
    events = get_events(HTML)
    assert len(events) == 20


def test_get_non_live_events():
    events = get_events(HTML)
    non_live_events = get_non_live_events(events)
    assert len(non_live_events) == 18


def test_get_event_datetime(event):
    event_datetime = get_event_datetime(event)
    assert event_datetime == datetime.datetime(year=2022, month=1, day=16, hour=8)


def test_get_team_names(event):
    assert get_team_names(event) == ["Young Ninjas", "Astralis Talent"]


def test_get_odds(event):
    assert get_odds(event) == [1.44, 2.66]


def test_get_tournament_name(event_with_tournament_name):
    assert get_tournament_name(event_with_tournament_name) == "Funspark ULTI 2021"

