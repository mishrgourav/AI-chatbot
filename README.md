# Neural Chat — Free Edition (powered by Google Gemini)
https://ai-chatbot-hhr5.onrender.com/
This version uses Google's Gemini API, which has a genuinely free tier —
no credit card required. Good for personal projects and learning.

## 1. Get a free API key
1. Go to https://aistudio.google.com/apikey
2. Sign in with any Google account
3. Click "Create API key"
4. Copy the key

No credit card, no billing setup needed.

## 2. Set up the project
```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

## 3. Add your API key
Create a new file named exactly `.env` in this folder (use the command
line to avoid Windows adding a hidden .txt extension):
```
notepad .env
```
Then paste this line in, replacing with your real key, and save:
```
GEMINI_API_KEY=your-key-here
```

**Never share this file or commit it to GitHub.**

## 4. Run it
```bash
python app.py
```
Open **http://127.0.0.1:5000**

## Free tier limits
Gemini's free tier (as of when this was written) allows a generous
number of requests per minute/day, which is plenty for personal/dev use.
If you ever hit a rate limit, just wait a minute and try again, or check
current limits at https://ai.google.dev/gemini-api/docs/rate-limits

## Notes
- Conversation history is kept in memory per browser tab while the
  server is running. Restarting `app.py` clears it.
- To change the chatbot's personality, edit `SYSTEM_PROMPT` near the
  top of `app.py`.
