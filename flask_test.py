import random
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, send_file

from nba_elo import nba_elo_parser

matplotlib.use("Agg")

app = Flask(__name__)

df = nba_elo_parser("./nba_schedule_and_results")
max_length = 0
for team, scores in df.items():
    if max_length < len(scores):
        max_length = len(scores)


@app.route("/stats")
def stats():
    for scores in df.values():
        while len(scores) < max_length:
            scores.append(np.nan)
    return pd.DataFrame(df).to_html()


@app.route("/")
def home():
    plt.figure(figsize=(15, 15))
    for team, scores in df.items():
        plt.plot(scores)
        plt.text(len(scores) - 1, scores[-1] + random.uniform(-1, 1) * 10, team)
    img = BytesIO()
    plt.savefig(img, format="png", dpi=200)
    img.seek(0)
    return send_file(img, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
