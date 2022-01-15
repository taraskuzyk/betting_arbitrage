from pprint import pprint

from database.orm.sport import Sport
from database.orm.website import Website
from definitions import ROOT_DIR
from scrape.betway.bets_extractor import BetsExtractor

HTML_PATH = ROOT_DIR / "scrape" / "betway" / "tests" / "betway_csgo.html"
with open(str(HTML_PATH), encoding="utf-8") as file:
    HTML = file.read()


def test_bets_extractor():
    bets_extractor = BetsExtractor(sport=Sport.csgo)
    bets = bets_extractor.extract_bets_from_page(HTML)
    for bet in bets:
        pprint(bet.__dict__)
    assert bets[0].team_1_name == "NIP"
