from arbitrage_finder.db_interface import DBInterface
from database import Database


class ArbitrageFinder:
    def __init__(self, db: Database):
        self.db_interface = DBInterface(db)

