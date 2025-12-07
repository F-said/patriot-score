import csv
import json

import os
from pathlib import Path

R_PATHS = [
    Path("data/responses/negative"),
    Path("data/responses/positive")
]

OUT_PATH = Path("data/responses/gpt5-responses.csv")

field_names = ["model", "confidence", "direction", "qnum", "question", "response", "reason"]
out_list = []

for path in R_PATHS:
    for root, dirs, files in os.walk(path):
        if files:
            conf_level = Path(root).name
            direction = Path(root).parent.name

            for f in files:
                print(root, f)
                model = Path(f).stem
                f_path = f"{root}/{f}"

                # TODO: holy nesting batman
                with open(f_path, 'r', errors="ignore") as file:
                    data = json.load(file)

                    for key, value in data.items():
                        row = {}
                        row["model"] = model
                        row["confidence"] = conf_level
                        row["direction"] = direction
                        row["qnum"] = key

                        row["question"] = value["original_question"]
                        row["response"] = value["final_response"]
                        row["reason"] = value["reasoning"].replace('\n', '')

                        out_list.append(row)

with open(OUT_PATH, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(out_list)
