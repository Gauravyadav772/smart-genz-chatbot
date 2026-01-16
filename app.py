from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


API_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "Groq backend running"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "user", "content": req.message}
            ],
            "temperature": 0.7,
            "max_tokens": 150
        }

        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return {"reply": f"Groq API error: {response.text}"}

        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        return {"reply": reply}

    except Exception as e:
        # Always return JSON (never crash UI)
        return {"reply": f"Server error: {str(e)}"}

