def calc_rating(elo_p1: int, records: list, k=16):
    encode = {"w": 1, "l": 0}

    for record, elo_oppo in records:
        expected_wins = 1 / (1 + 10 ** ((elo_oppo - elo_p1) / 400))

        print(elo_oppo, expected_wins)
        elo_p1 = elo_p1 + k * (encode[record] - expected_wins)

    return elo_p1

