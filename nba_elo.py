from elo_rating import ELOMaker
import datetime
import csv

import pandas as pd


def nba_elo_parser(path: str):
    elomaker = ELOMaker()
    names = {"january": 13, "november": 11, "october": 10, "december": 12}

    for csv_file, number in sorted(names.items(), key=(lambda x: x[1])):
        csv_path = f"{path}/{csv_file}.csv"
        csv_df = read_file(csv_path, elomaker)
        teams = list(csv_df["wins"].unique())
        teams += list(csv_df["loses"].unique())
        teams = set(teams)
        elomaker.teams.init_teams(teams)
        csv_df = elomaker.assign_rating(csv_df)

    return elomaker.teams.teams_elo


def winorlose(row: dict):
    if int(row["visitorPoints"]) > int(row["homePoints"]):
        return (
            row["visitor"],
            row["home"],
            row.get("visitorPoints", 0),
            row.get("homePoints", 0),
        )
    else:
        return (
            row["home"],
            row["visitor"],
            row.get("homePoints", 0),
            row.get("visitorPoints", 0),
        )


def read_file(csv_path: str, elomaker):
    cal = {"Dec": 12, "Nov": 11, "Oct": 10, "Jan": 1}
    res_df = {
        "dates": list(),
        "wins": list(),
        "loses": list(),
        "winsPoints": list(),
        "losesPoints": list(),
    }
    with open(csv_path) as filepath:
        next(filepath)
        data = csv.DictReader(
            filepath,
            fieldnames=[
                "Date",
                "start",
                "visitor",
                "visitorPoints",
                "home",
                "homePoints",
            ],
        )
        for row in data:
            winner, loser, w_points, l_points = winorlose(row)
            _, month, day, year = row["Date"].split()
            date = datetime.date(int(year), cal[month], int(day))
            res_df["dates"].append(date)
            res_df["wins"].append(winner)
            res_df["loses"].append(loser)
            res_df["winsPoints"].append(w_points)
            res_df["losesPoints"].append(l_points)

        res_df = pd.DataFrame(res_df)

        return res_df


if __name__ == "__main__":
    import sys

    print(nba_elo_parser(sys.argv[1]))
