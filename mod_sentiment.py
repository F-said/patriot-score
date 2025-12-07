from scripts.gen_qs import Generator

import csv

from pathlib import Path

Q_PATHS = [
    Path("data/questions/negative"),
    Path("data/questions/positive")
]

for path in Q_PATHS:
    with open(f"{path}/base.csv") as file:
        reader = csv.reader(file)

        # pass human generated questions to interface
        list_qs = [row[0] for row in list(reader)]
        questions = Generator(list_qs, path)
        # vary sentiment
        questions.vary_sentiment()
