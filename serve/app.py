from flask import Flask, request, jsonify
import openai
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Load prompt version
with open('../prompts/v1.json') as f:
    prompt_template = json.load(f)['prompt']

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("input")
    prompt = prompt_template.replace("{{input}}", user_input)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response['choices'][0]['message']['content'].strip()

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "input": user_input,
        "response": reply
    }
    with open("logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
