import pytest
from elo_rating import calc_rating


def test_elo_rating():
    observation = [("w", 1500), ("w", 1500), ("l", 1500), ("w", 1500)]  ## 4연승
    A_rating = 1500
    # B_rating = 1500

    adjusted_A_rating = calc_rating(A_rating, observation)

    print(adjusted_A_rating)


def test_get_history():
    pass
