from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
import uuid

from utils.ai_handler import ask_ai
from utils.helpers import build_quiz_prompt, clean_text
from utils.db import get_db_connection
from routes.upload_routes import _get_store as _get_upload_store

quiz_bp = Blueprint("quiz", __name__)


@quiz_bp.route("/", methods=["GET", "POST"])
def quiz():
    if "user_id" not in session:
        if request.method == "POST":
            return jsonify({"error": "Please log in first."}), 401
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("dashboard/quiz.html")

    upload_store = _get_upload_store()
    text = clean_text(upload_store.get("text", ""))

    if not text.strip():
        return jsonify({"error": "Please upload a PDF first to generate a quiz."}), 400

    payload = request.get_json(silent=True) or {}
    try:
        question_count = int(payload.get("question_count", 5))
    except (ValueError, TypeError):
        question_count = 5

    prompt = build_quiz_prompt(text, question_count)
    result = ask_ai(prompt)

    user_id = session.get("user_id")
    file_id = upload_store.get("file_id")

    if user_id and result and not result.startswith("OpenRouter error") and not result.startswith("Error:"):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO quizzes (user_id, file_id, quiz_type, questions_json)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, file_id, f"{question_count}-MCQs", result)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Warning: Could not save quiz to DB: {e}")

    return jsonify({"quiz": result})