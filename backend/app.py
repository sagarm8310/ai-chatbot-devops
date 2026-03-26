from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@app.route('/')
def home():
    return "AI Backend is running!"

# 🔥 Weather function
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return "Unable to fetch weather."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"The weather in {city} is {desc} with temperature {temp}°C."

    except Exception as e:
        print("Weather Error:", e)
        return "Error fetching weather data."

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    # 🔥 Weather detection (NEW)
    if "weather" in user_message.lower():
        try:
            # extract city (simple logic)
            if "in" in user_message.lower():
                city = user_message.lower().split("in")[-1].strip()
            else:
                city = "Bangalore"  # default

            weather_reply = get_weather(city)
            return jsonify({"reply": weather_reply})

        except Exception as e:
            print("Weather Route Error:", e)

    # 🔥 OpenRouter (existing logic)
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)