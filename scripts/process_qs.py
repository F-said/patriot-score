import requests


class Interface:
    def __init__(self, questions):
        self.questions = questions
        self.dev_prompt ="""
        For each question, evaluate supporting points that utilize historical evidence for both sides of this argument, 
        evaluate these arguments, and conclude with a definitive ‘yes’ or ‘no’ answer.
        """
    
    def process(self, client, model):
        for q in self.questions:
            print(q[0])
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "developer", "content": self.dev_prompt},
                    {"role": "user", "content": q[0]}
                ]
            )

            print(completion.choices[0].message)

