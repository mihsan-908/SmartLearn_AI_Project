import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def ask_ai(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "Error: OPENROUTER_API_KEY is not set in your .env file."

    model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat")
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "SmartLearn AI"
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are SmartLearn AI, a friendly human-like study assistant. "
                    "Answer naturally, clearly, and helpfully. Avoid robotic wording."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1200
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)

        if response.status_code != 200:
            return f"OpenRouter error {response.status_code}: {response.text}"

        result = response.json()

        choices = result.get("choices")
        if not choices:
            return f"Unexpected API response: {result}"

        message = choices[0].get("message", {})
        content = message.get("content")

        if not content:
            return f"Empty AI response: {result}"

        return content

    except requests.exceptions.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"