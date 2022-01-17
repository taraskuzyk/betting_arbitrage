from pprint import pprint

from enums.sport import Sport
from definitions import ROOT_DIR
from scrape.betway.bets_extractor import BetsExtractor

HTML_PATH = ROOT_DIR / "scrape" / "betway" / "tests" / "betway_csgo.html"
with open(str(HTML_PATH), encoding="utf-8") as file:
    HTML = file.read()

HTML_PATH_LIVE = (
    ROOT_DIR / "scrape" / "betway" / "tests" / "betway_csgo_with_live_match.html"
)
with open(str(HTML_PATH_LIVE), encoding="utf-8") as file:
    HTML_LIVE = file.read()


def test_bets_extractor():
    bets_extractor = BetsExtractor(sport=Sport.csgo)
    bets = bets_extractor.extract_bets_from_page(HTML)
    for bet in bets:
        pprint(bet.__dict__)
    assert bets[0].team_1_name == "NIP"


def test_bets_extractor_with_live_match():
    bets_extractor = BetsExtractor(sport=Sport.csgo)
    bets = bets_extractor.extract_bets_from_page(HTML_LIVE)
    for bet in bets:
        pprint(bet.__dict__)
    assert bets[0].team_1_name == "G2"
