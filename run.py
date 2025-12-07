from scripts.process_qs import Interface

import csv

from openai import OpenAI
from google import genai
import os

from pathlib import Path


client_openai = OpenAI()

client_deep = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

client_grok = OpenAI(
  api_key=os.getenv("XAI_API_KEY"),
  base_url="https://api.x.ai/v1"
)

client_gem = genai.Client()

Q_PATHS = [
    Path("data/questions/negative"),
    Path("data/questions/positive")
]

for path in Q_PATHS:
    # process each sentiment
    files = os.listdir(path)

    for f in files:
        with open(f"{path}/{f}") as file:
            reader = csv.reader(file)

            # pass questions to interface
            questions = Interface(list(reader), f"{path.name}/{Path(f).stem}")

        #print("\nProcessing OpenAI")
        #questions.process(client_openai, "gpt-4o-mini")

        #print("\nProcessing Deep-Seek")
        #questions.process(client_deep, "deepseek-chat")

        #print("\nProcessing Grok")
        #questions.process(client_grok, "grok-4")

        #print("\nProcessing Gemini")
        #questions.process(client_gem, "gemini-1.5-flash")

        print("\nProcessing OpenAI")
        questions.process(client_openai, "gpt-5-nano")
