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
CRICKET_API_KEY = os.getenv("CRICKET_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@app.route('/')
def home():
    return "AI Backend is running!"

# 🌦 WEATHER FUNCTION
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url)
        data = res.json()

        if res.status_code != 200:
            return "❌ Unable to fetch weather."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"🌤 Weather in {city.title()}: {temp}°C, {desc}"

    except Exception as e:
        print("Weather Error:", e)
        return "❌ Error fetching weather."

# 🏏 CRICKET FUNCTION
def get_cricket():
    try:
        url = f"https://api.cricapi.com/v1/currentMatches?apikey={CRICKET_API_KEY}"
        res = requests.get(url)
        data = res.json()

        matches = data.get("data", [])

        if matches:
            match = matches[0]
            name = match.get("name")
            status = match.get("status")
            venue = match.get("venue")

            return f"🏏 {name}\n📊 {status}\n📍 {venue}"

        return "🏏 No live matches available."

    except Exception as e:
        print("Cricket Error:", e)
        return "❌ Error fetching cricket data."

# 📰 NEWS FUNCTION (UPDATED 🔥)
def get_news(query="india"):
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
        res = requests.get(url)
        data = res.json()

        articles = data.get("articles", [])[:3]

        if not articles:
            return f"📰 No news found for '{query}'."

        reply = f"📰 Top News about {query}:\n\n"
        for art in articles:
            reply += f"• {art['title']}\n"

        return reply

    except Exception as e:
        print("News Error:", e)
        return "❌ Error fetching news."

# 🤖 MAIN CHAT ROUTE
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    msg = user_message.lower()

    # 🧠 SMART DETECTION

    # 🌦 WEATHER
    if any(word in msg for word in ["weather", "temperature", "climate"]):
        if " in " in msg:
            city = msg.split(" in ")[-1].strip()
        else:
            city = "Bangalore"
        return jsonify({"reply": get_weather(city)})

    # 🏏 CRICKET (ONLY REAL-TIME)
    elif any(word in msg for word in ["live score", "current match", "live cricket", "score update"]):
        return jsonify({"reply": get_cricket()})

    # 📰 NEWS (UPDATED 🔥)
    elif "news" in msg:
        # extract topic
        query = msg.replace("latest", "").replace("news", "").strip()

        if query:
            return jsonify({"reply": get_news(query)})
        else:
            return jsonify({"reply": get_news("india")})

    # 🤖 AI FALLBACK (OpenRouter)
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

        if response.status_code != 200:
            reply = "❌ API Error"
        else:
            reply = data["choices"][0]["message"]["content"]

    except Exception as e:
        print("AI Error:", e)
        reply = "❌ Error communicating with AI."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)