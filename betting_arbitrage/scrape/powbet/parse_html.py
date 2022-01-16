from bs4 import BeautifulSoup


def get_tournaments(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.select(selector='._asb_expansion-panel._asb_events-tree-table-node-CH ', recursive=False)


def get_tournament_name(tournament_element):
    return tournament_element.select_one(".asb-pos-wide.asb-text._asb_events-tree-table-node-CH-name").text


def get_events(tournament):
    return tournament.select("._asb_events-table-row")


def get_teams_in_event(event_element):
    return [team_name.text for team_name in event_element.select("._asb_events-table-row-competitors-column .asb-text")]


def get_odds_in_event(event_element):
    return [float(odds.text) for odds in event_element.select("._asb_price-block span")]


def get_event_datetime_str(event_element):
    return event_element.select_one("._asb_events-table-row--start-datetime").text.replace('• ', '')


