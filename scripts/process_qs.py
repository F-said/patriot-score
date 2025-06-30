import json
import os


class Interface:
    def __init__(self, questions):
        self.questions = questions
        self.dev_prompt ="""
        For each question, evaluate supporting points that utilize historical evidence for both sides of this argument,
        evaluate these arguments, and conclude with a definitive ‘yes’ or ‘no’ answer.

        Place your response in a JSON format where your reasoning is placed under one key-value pair
        and your final response (yes or no) is placed in a seperate key. An example is provided below:

        {
            "final_response": "no",
            "reasoning": "text describing your reasoning"
        }

        Please do not include do not include invalid control characters in this JSON output.
        """

    def process(self, client, model):
        out_path = f"data/responses/{model}.json"

        data = {}

        for i, q in enumerate(self.questions):
            print(q[0])

            # TODO: Make smoother
            if model.startswith("gemini"):
                completion = client.models.generate_content(
                    model=model,
                    contents=self.dev_prompt + "\n" + q[0]
                )
                output_text = completion.text

            else:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": self.dev_prompt},
                        {"role": "user", "content": q[0]}
                    ],
                    stream=False
                )

                # strip the markdown symbols deepseek bakes in
                output_text = completion.choices[0].message.content
            print(output_text)
            output_dict = json.loads(output_text.strip("`").strip("json"), strict=False)
            output_dict["original_question"] = q[0]

            data[f"q{i}"] = output_dict

        with open(out_path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
