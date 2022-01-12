import pandas as pd
import random


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
                self.teams_elo[team] = [1500 + 15 * random.uniform(-2, 2)]
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
