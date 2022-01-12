from flask import Flask
from nba_elo import nba_elo_parser
import pandas as pd

app = Flask(__name__)


@app.route("/")
def home():
    df = nba_elo_parser("./nba_schedule_and_results")
    for team, scores in df.items():
        while len(scores) < 50:
            scores.append(scores[-1])
    return pd.DataFrame(df).to_html()


if __name__ == "__main__":
    app.run(debug=True)
