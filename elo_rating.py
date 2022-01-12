import csv
import datetime
import pandas as pd


class Teams:
    def __init__(self):
        self.teams_elo = dict()
        self.teams_games = dict()

    def get_teams_elo(self):
        return self.teams_elo

    def get_teams_games(self):
        return self.teams_games

    def init_teams(self, teams: list):
        for team in teams:
            if team not in self.teams_elo:
                self.teams_elo[team] = [1500]
                self.teams_games[team] = 0

    def adjust(self, name, score):
        self.teams_elo[name].append(score)
        self.teams_games[name] += 1

    def get_score(self, name):
        return self.teams_elo[name][-1]

    def get_games(self, name):
        return self.teams_games[name]


class ELOMaker:
    def __init__(self) -> None:
        self.teams = Teams()

    def read_nba_data(self, path: str) -> None:
        names = {"january": 13, "november": 11, "october": 10, "december": 12}

        for csv_file, number in sorted(names.items(), key=(lambda x: x[1])):
            csv_path = f"{path}/{csv_file}.csv"
            csv_df = self.read_file(csv_path)
            teams = list(csv_df["wins"].unique())
            teams += list(csv_df["loses"].unique())
            teams = set(teams)
            self.teams.init_teams(teams)
            csv_df = self.assign_rating(csv_df)

        return self.teams

    def assign_rating(self, dataframe: pd.DataFrame):
        winner_rating = list()
        loser_rating = list()
        for _, row in dataframe.iterrows():
            winner = row["wins"]
            loser = row["loses"]

            winner_elo, loser_elo = self.adjusted_rating(winner, loser)
            winner_rating.append(winner_elo)
            loser_rating.append(loser_elo)
            self.teams.adjust(winner, winner_elo)
            self.teams.adjust(loser, loser_elo)

        dataframe["winnerRating"] = winner_rating
        dataframe["loserRating"] = loser_rating

        return dataframe

    def adjusted_rating(self, winner, loser, k=32):
        elo_win, elo_lose = self.teams.get_score(winner), self.teams.get_score(loser)
        expected_wins = 1 / (1 + 10 ** ((elo_win - elo_lose) / 400))
        expected_lose = 1 / (1 + 10 ** ((elo_lose - elo_win) / 400))
        elo_win = elo_win + k * (1 - expected_wins)
        elo_lose = elo_lose + k * (0 - expected_lose)

        return elo_win, elo_lose

    def adjusted_rating_double(self, winners, losers, k=16):
        elo_wins, elo_loses = 1, 2
        return elo_wins, elo_loses

    def read_file(self, csv_path: str):
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
                winner, loser, w_points, l_points = self.winorlose(row)
                _, month, day, year = row["Date"].split()
                date = datetime.date(int(year), cal[month], int(day))
                res_df["dates"].append(date)
                res_df["wins"].append(winner)
                res_df["loses"].append(loser)
                res_df["winsPoints"].append(w_points)
                res_df["losesPoints"].append(l_points)

        res_df = pd.DataFrame(res_df)

        return res_df

    def winorlose(self, row: dict):
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


if __name__ == "__main__":
    import sys

    OBJ = ELOMaker()

    OBJ.read_nba_data(sys.argv[1])
