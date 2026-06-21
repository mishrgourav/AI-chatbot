"""
app.py
Flask backend serving a chatbot powered by Google's Gemini API (free tier).

Setup:
    1. pip install -r requirements.txt
    2. Create a .env file in this folder with:
           GEMINI_API_KEY=your-key-here
    3. python app.py
Then open http://127.0.0.1:5000 in your browser.

Get a free API key (no credit card required) at:
    https://aistudio.google.com/apikey
"""

import os

from google import genai
from google.genai import types
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

load_dotenv()  # reads GEMINI_API_KEY from a local .env file

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Create a .env file in this folder "
        "with the line: GEMINI_API_KEY=your-key-here\n"
        "Get a free key at https://aistudio.google.com/apikey"
    )

client = genai.Client(api_key=API_KEY)
app = Flask(__name__)

# Keeps conversation history per browser session (in-memory only —
# resets when the server restarts). Fine for local/dev use.
conversation_history = {}

SYSTEM_PROMPT = (
    "You are a friendly, helpful chatbot embedded in a web page. "
    "Keep replies conversational and reasonably concise."
)

MODEL_NAME = "gemini-2.5-flash"  # fast, free-tier friendly


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "default")

    if not message:
        return jsonify({"response": "Please type something!"}), 400

    history = conversation_history.setdefault(session_id, [])
    history.append(types.Content(role="user", parts=[types.Part(text=message)]))

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=1024,
            ),
        )
        reply = response.text or "Sorry, I didn't get a response. Try again?"
    except Exception as e:
        # Don't crash the server on API errors (bad key, rate limit, etc.)
        print(f"Gemini API error: {e}")
        return jsonify({
            "response": "Sorry, I had trouble reaching the AI service. "
                        "Check your API key and internet connection."
        }), 502

    history.append(types.Content(role="model", parts=[types.Part(text=reply)]))

    # Keep history from growing forever
    if len(history) > 20:
        conversation_history[session_id] = history[-20:]

    return jsonify({"response": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
