from arbitrage_calculator import (
    Bet,
    get_implied_probability_of_a_bet,
    lowest_implied_probability_from_bet_pair,
    is_arbitrage_possible,
    find_pairs_of_bets_with_possible_arbitrage,
    get_combinations_of_bets,
)


def test_if_calculates_profit_ratio_properly():
    bet_1 = Bet(team_1_odds=1.1, team_2_odds=10)
    bet_2 = Bet(team_1_odds=1.5, team_2_odds=5)


def test_implied_probability_without_draw():
    assert get_implied_probability_of_a_bet(2, 5) == 0.7


def test_implied_probability_with_draw():
    assert get_implied_probability_of_a_bet(2, 5, 20) == 0.75


def test_lowest_implied_probability_from_bet():
    bet_1 = Bet(team_1_odds=1.45, team_2_odds=2.55)
    bet_2 = Bet(team_1_odds=1.5, team_2_odds=2.51)
    implied_prob = lowest_implied_probability_from_bet_pair(bet_1, bet_2)
    implied_prob_rounded = round(implied_prob, ndigits=2)
    assert implied_prob_rounded == 1.06


def test_lowest_implied_probability_from_bet_good_odds():
    bet_1 = Bet(team_1_odds=1.2, team_2_odds=8)
    bet_2 = Bet(team_1_odds=2.0, team_2_odds=1.4)
    implied_prob = lowest_implied_probability_from_bet_pair(bet_1, bet_2)
    implied_prob_rounded = round(implied_prob, ndigits=2)
    assert implied_prob_rounded == 0.62


def test_is_arbitrage_possible():
    bet_1 = Bet(team_1_odds=1.2, team_2_odds=8)
    bet_2 = Bet(team_1_odds=2.0, team_2_odds=1.4)
    assert is_arbitrage_possible(bet_1, bet_2)


def test_is_arbitrage_possible_with_margin():
    bet_1 = Bet(team_1_odds=1.2, team_2_odds=8)
    bet_2 = Bet(team_1_odds=2.0, team_2_odds=1.4)
    assert not is_arbitrage_possible(bet_1, bet_2, margin=0.7)


def test_get_combinations_of_bets():
    bets = [Bet(1, 2, 1.5), Bet(2, 1.5, 2), Bet(3, 0.5, 0.5)]

    combinations = get_combinations_of_bets(bets)
    assert len(combinations) == 3


def test_find_pairs_of_bets_with_possible_arbitrage():
    bets = [
        Bet(id=1, team_1_odds=1.2, team_2_odds=8),
        Bet(id=2, team_1_odds=2.0, team_2_odds=1.4),
        Bet(id=3, team_1_odds=0.5, team_2_odds=0.5),
    ]

    list_of_bets_with_possible_arbitrage = find_pairs_of_bets_with_possible_arbitrage(
        bets
    )
    pair_of_bets = list_of_bets_with_possible_arbitrage[0]
    ids_of_bets = [pair_of_bets[0].id, pair_of_bets[1].id]
    assert len(list_of_bets_with_possible_arbitrage) == 1 and all(
        bet_id in [1, 2] for bet_id in ids_of_bets
    )
