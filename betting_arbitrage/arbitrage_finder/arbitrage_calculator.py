from dataclasses import dataclass
from typing import List, Tuple
from itertools import permutations


@dataclass
class Bet:
    id: int = None
    team_1_odds: float = None
    team_2_odds: float = None


def find_pairs_of_bets_with_possible_arbitrage(
    bets: List[Bet], margin: float = 0
) -> List[Tuple[Bet, Bet]]:
    combinations_of_bets = get_combinations_of_bets(bets)
    return [
        combo for combo in combinations_of_bets if is_arbitrage_possible(*combo, margin=margin)
    ]


def get_combinations_of_bets(bets: List[Bet]) -> List[Tuple[Bet, Bet]]:
    combinations_of_bets = []
    while bets:
        bet = bets.pop()
        combinations_of_bets.extend(_get_combinations_of_a_bet_with_bets(bet, bets))
    return combinations_of_bets


def _get_combinations_of_a_bet_with_bets(
    bet: Bet, bets: List[Bet]
) -> List[Tuple[Bet, Bet]]:
    return [(bet, other_bet) for other_bet in bets]


def is_arbitrage_possible(bet_1: Bet, bet_2: Bet, margin: float = 0):
    return lowest_implied_probability_from_bet_pair(bet_1, bet_2) + margin < 1


def lowest_implied_probability_from_bet_pair(bet_1: Bet, bet_2: Bet) -> float:
    first_implied_probability = get_implied_probability_of_a_bet(
        bet_1.team_1_odds, bet_2.team_2_odds
    )
    second_implied_probability = get_implied_probability_of_a_bet(
        bet_2.team_1_odds, bet_1.team_2_odds
    )
    if first_implied_probability <= second_implied_probability:
        return first_implied_probability
    return second_implied_probability


def get_implied_probability_of_a_bet(
    team_1_win: float, team_2_win: float, draw: float = None
) -> float:
    if team_1_win == 0 or team_2_win == 0 or draw == 0:
        raise ValueError('INPUTS CANT BE NULL!!!')
    implied_probability = 1 / team_1_win + 1 / team_2_win
    if draw is not None:
        implied_probability += 1 / draw
    return implied_probability
