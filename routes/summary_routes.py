from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
import uuid

from utils.ai_handler import ask_ai
from utils.helpers import build_summary_prompt, clean_text
from utils.db import get_db_connection
from routes.upload_routes import _get_store as _get_upload_store

summary_bp = Blueprint("summary", __name__)


@summary_bp.route("/", methods=["GET", "POST"])
def summary():
    if "user_id" not in session:
        if request.method == "POST":
            return jsonify({"error": "Please log in first."}), 401
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("dashboard/summary.html")

    upload_store = _get_upload_store()
    pdf_text = clean_text(upload_store.get("text", ""))

    if not pdf_text.strip():
        return jsonify({"error": "Please upload a PDF first to generate a summary."}), 400

    payload = request.get_json(silent=True) or {}
    summary_type = payload.get("summary_type", "bullet")

    prompt = build_summary_prompt(pdf_text, summary_type)
    result = ask_ai(prompt)

    user_id = session.get("user_id")
    file_id = upload_store.get("file_id")

    if user_id and result and not result.startswith("OpenRouter error") and not result.startswith("Error:"):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO summaries (user_id, file_id, summary_type, generated_summary)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, file_id, summary_type, result)
            )
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Warning: Could not save summary to DB: {e}")

    return jsonify({
        "summary": result,
        "summary_type": summary_type
    })