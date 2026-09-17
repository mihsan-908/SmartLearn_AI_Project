import os
import re
from datetime import datetime

ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_folder(path):
    os.makedirs(path, exist_ok=True)
    return path

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def truncate_text(text, limit=12000):
    if not text:
        return ""
    return text[:limit]

def build_summary_prompt(text, summary_type="bullet"):
    text = truncate_text(clean_text(text))

    if summary_type == "short":
        instruction = "Give a short and simple summary in 5-6 lines."
    elif summary_type == "detailed":
        instruction = "Give a detailed summary with headings and explanations."
    else:
        instruction = "Give the summary in clear bullet points."

    return f"""
You are SmartLearn AI, a helpful study assistant.
respond like humans.

Task:
{instruction}

Content:
{text}
"""

def build_quiz_prompt(text, question_count=5):
    text = truncate_text(clean_text(text))

    return f"""
Create {question_count} MCQs from the following content.
Return the questions in a clean numbered format with options A, B, C, D and the correct answer.

Content:
{text}
"""

def build_notes_prompt(text):
    text = truncate_text(clean_text(text))

    return f"""
Turn the following content into easy exam notes with headings and bullet points.

Content:
{text}
"""

def format_time(value=None):
    value = value or datetime.now()
    return value.strftime("%Y-%m-%d %H:%M:%S")