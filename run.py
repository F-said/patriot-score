from scripts.process_qs import Interface

import csv

from openai import OpenAI
from google import genai
import os


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

with open('data/questions.csv', 'r') as file:
    reader = csv.reader(file)

    # pass questions to interface
    questions = Interface(list(reader))

print("\nProcessing OpenAI")
#questions.process(client_openai, "gpt-4o-mini")

print("\nProcessing Deep-Seek")
#questions.process(client_deep, "deepseek-chat")

print("\nProcessing Grok")
#questions.process(client_grok, "grok-3")

print("\nProcessing Gemini")
questions.process(client_gem, "gemini-2.5-flash")
