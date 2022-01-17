from pprint import pprint

from enums.sport import Sport
from definitions import ROOT_DIR
from scrape.gg_bet.bets_extractor import BetsExtractor

HTML_PATH = ROOT_DIR / "scrape" / "gg_bet" / "tests" / "gg_bet_csgo.html"
with open(str(HTML_PATH), encoding="utf-8") as file:
    HTML = file.read()


def test_bets_extractor():
    bets_extractor = BetsExtractor(sport=Sport.csgo)
    bets = bets_extractor.extract_bets_from_page(HTML)
    for bet in bets:
        pprint(bet.__dict__)
    assert bets[0].team_1_name == "Young Ninjas"
