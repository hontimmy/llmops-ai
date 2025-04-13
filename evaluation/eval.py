import json
import openai
from difflib import SequenceMatcher
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def run_eval():
    with open('../prompts/v1.json') as f:
        prompt_template = json.load(f)['prompt']
    with open('eval_dataset.json') as f:
        dataset = json.load(f)

    scores = []
    for item in dataset:
        prompt = prompt_template.replace("{{input}}", item["input"])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        output = response['choices'][0]['message']['content'].strip()
        score = similarity(output, item["expected"])
        scores.append(score)
        print(f"Input: {item['input']}, Expected: {item['expected']}, Got: {output}, Score: {score:.2f}")

    print(f"\nAverage Similarity Score: {sum(scores)/len(scores):.2f}")

if __name__ == "__main__":
    run_eval()
