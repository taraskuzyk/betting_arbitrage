from typing import List

from database import Database, orm
from scrape.shared import Bet


class DBInterface:
    def __init__(self, db: Database):
        self.db = db

    def add_bets_to_db(self, bets: List[Bet]):
        orm_bets = [orm.Bet(**bet.__dict__) for bet in bets]
        self.db.add_all(orm_bets, commit=True)