from _pytest.fixtures import yield_fixture
import pytest
from elo_rating import Teams


@pytest.fixture(scope="class")
def team_obj():
    res = Teams()
    yield res
    del res


def elo_obj():
    res = Teams()
    yield res
    del res


def test_init_teams(team_obj):
    obs = ["a", "b", "c"]
    pred_elo = {"a": 1500, "b": 1500, "c": 1500}
    pred_games = {"a": 0, "b": 0, "c": 0}

    team_obj.init_teams(obs)

    assert team_obj.teams_elo == pred_elo
    assert team_obj.teams_games == pred_games


def test_