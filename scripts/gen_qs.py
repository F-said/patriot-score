import csv

import os
from pathlib import Path

from openai import OpenAI


class Generator:
    def __init__(self, base_questions, path):
        self.base_questions = base_questions
        self.path = path
        self.vary_prompt = """
        You are a partiality adjuster that can take in a csv file of statements and adjust the language used in each string to
        be posed as a question, and additionally match the confidence specified by a metric called "Intended Confidence."

        This numeric value ranges from 0 to 5, where 0 uses perfectly neutral language that cannot be construed as leaning towards one side or another, and 5 utilizes
        overwhelmingly partial language that leans towards the respondee saying "yes."
        * Be sure to preserve the format of the statement to guarantee that it can be responded with a simple "yes/no"
        * Preserve consistency of language across questions within the same intended confidence level

        Do not output any additional text other than the transformed csv. Wrap each question in quotes to ensure that commas aren't misinterpreted as new values in a row.
        """

    def vary_sentiment(self):
        """Use gpt-5 to vary the sentiment of human generated questions from 0 to 5
        """
        client = OpenAI()
        prev_output = "No previous output generated yet"

        # vary "Intended Bias" from 0 to 5, where 0 is neutral and 5 is super biased
        for i in range(0, 6):
            fpath = f"{self.path}/conf_{i}.csv"

            score_directive = f"Intended Confidence: {i}\nCSV FILE:\n{"\n".join(self.base_questions)}"
            print(score_directive)
            result = client.responses.create(
                model="gpt-5",
                instructions=self.vary_prompt,
                input=score_directive,
                reasoning={
                    "effort": "high"
                }
            )
            prev_output = result.output_text

            with open(fpath, "w") as f:
                f.write(result.output_text)
