from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Get your Groq API key from environment variable (safer than hardcoding)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a friendly, human-like AI chatbot."},
            {"role": "user", "content": user_message}
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions",
                             json=payload, headers=headers)

    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
    else:
        reply = "⚠️ Error: Could not reach Groq API."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
