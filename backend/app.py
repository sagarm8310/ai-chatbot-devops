from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route('/')
def home():
    return "AI Backend is running!"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "stepfun/step-3.5-flash",
                "messages": [
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 500
            }
        )

        data = response.json()
        print("API RESPONSE:", data)

        if response.status_code != 200:
            reply = f"API Error: {data.get('error', {}).get('message', 'Unknown error')}"
        else:
            reply = data["choices"][0]["message"]["content"]

    except Exception as e:
        print("ERROR:", e)
        reply = "Error communicating with AI."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)