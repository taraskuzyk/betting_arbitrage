from typing import List

import scrape.betway as betway
import scrape.powbet as powbet
import scrape.gg_bet as gg_bet
from database import Database
from database.orm import Base
from definitions import ROOT_DIR
from enums.sport import Sport
from scrape.db_interface import DBInterface

# db_main = Database(url=f"sqlite:///{str(db_path)}", metadata=Base.metadata)
from scrape.shared import Bet


class BetsDownloader:
    def __init__(self, db: Database, extractors: List):
        self.extractors = extractors
        self.db = db

    def download_latest_bets_for_sport(self, sport):
        for extractor in self.extractors:
            bets_extractor = extractor(db=self.db, sport=sport)
            bets_extractor.run()


if __name__ == "__main__":
    db = Database(
        url=f"sqlite:///{str(ROOT_DIR / 'betting_odds.db')}",
        metadata=Base.metadata,
        # should_create_schema=True,
    )

    bets_downloader = BetsDownloader(
        db,
        extractors=[
            # betway.bets_extractor.BetsExtractor,
            # powbet.bets_extractor.BetsExtractor,
            gg_bet.bets_extractor.BetsExtractor,
        ],
    )
    bets_downloader.download_latest_bets_for_sport(Sport.csgo)
