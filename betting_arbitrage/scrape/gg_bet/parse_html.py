from datetime import datetime

from bs4 import BeautifulSoup


def get_events(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.select(
        selector='div[class*="sportEventRow__container"]', recursive=False
    )


def get_non_live_events(events):
    return [
        event
        for event in events
        if event.select_one(selector='div[class*="futureDate"]') is not None
    ]


def get_event_datetime(event):
    date_str = event.select_one(selector='div[class*="DateTime-date"]').text
    time_str = date_str[:5]
    date_str = date_str.replace(time_str, "")
    date_str = time_str + " " + date_str + " " + str(datetime.now().year)
    return datetime.strptime(date_str, "%H:%M %b %d %Y")


def get_team_names(event):
    team_selectors = event.select(selector='div[class*="__name__"]')
    return [selector.text for selector in team_selectors]


def get_odds(event):
    odds_selectors = event.select(selector='[class*="app-Odd-button"]')
    odds_selectors = odds_selectors[:2]
    return [float(selector.text) for selector in odds_selectors]


def get_tournament_name(event):
    return event.select_one(selector='[class*="TournamentName"]').text
