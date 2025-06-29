from scripts.process_qs import Interface

import csv

from openai import OpenAI
import os


client_openai = OpenAI()
client_deep = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

with open('data/questions.csv', 'r') as file:
    reader = csv.reader(file)
    
    # pass questions to interface
    questions = Interface(reader)
    # process questions for open-ai
    print("\nProcessing OpenAI")
    questions.process(client_openai, "gpt-4o-mini")

    # process questions for deep-seek
    print("\nProcessing Deep-Seek")
    questions.process(client_deep, "deepseek-chat")