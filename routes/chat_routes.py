from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
import uuid

from utils.ai_handler import ask_ai
from utils.helpers import clean_text, truncate_text
from utils.db import get_db_connection
from routes.upload_routes import pdf_text_storage, _get_store as _get_upload_store

chat_bp = Blueprint("chat", __name__)

# Per-user in-memory chat history
chat_memory = {}


def _get_client_id():
    if "client_id" not in session:
        session["client_id"] = str(uuid.uuid4())
    return session["client_id"]


def _get_store():
    client_id = _get_client_id()
    if client_id not in chat_memory:
        chat_memory[client_id] = {
            "messages": []
        }
        user_id = session.get("user_id")
        if user_id:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT user_message, ai_response 
                    FROM chats 
                    WHERE user_id = %s 
                    ORDER BY created_at ASC LIMIT 50
                    """,
                    (user_id,)
                )
                rows = cur.fetchall()
                cur.close()
                conn.close()
                for row in rows:
                    chat_memory[client_id]["messages"].append({"role": "user", "content": row["user_message"]})
                    chat_memory[client_id]["messages"].append({"role": "ai", "content": row["ai_response"]})
            except Exception:
                pass
    return chat_memory[client_id]


@chat_bp.route("/", methods=["GET", "POST"])
def chat():
    if "user_id" not in session:
        if request.method == "POST":
            return jsonify({"error": "Please log in to chat."}), 401
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        return render_template("dashboard/chat.html")

    store = _get_store()
    client_id = _get_client_id()
    user_id = session.get("user_id")

    payload = request.get_json(silent=True) or {}
    user_message = clean_text(payload.get("message", ""))

    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    upload_store = _get_upload_store()
    pdf_text = truncate_text(clean_text(upload_store.get("text", "")), 12000)
    file_id = upload_store.get("file_id")

    if pdf_text:
        prompt = f"""
You are SmartLearn AI, a helpful study assistant.
Respond like humans.
Use the following PDF content to answer the user's question.

PDF Content:
{pdf_text}

User Question:
{user_message}

Instructions:
- Answer clearly and simply.
- If the answer is in the document, use it.
- If not, give the best helpful response based on the context.
- Respond like humans. Do not mention that you are an AI or that the answer is based on the PDF. Just answer naturally.
"""
    else:
        prompt = f"""
You are SmartLearn AI, a helpful study assistant.
Respond like humans.

User Question:
{user_message}

Instructions:
- Answer clearly and simply.
- If the user asks about uploaded notes, explain that no PDF has been uploaded yet.
- Respond like humans. Do not mention that you are an AI. Just answer naturally.
"""

    store["messages"].append({"role": "user", "content": user_message})

    try:
        ai_response = ask_ai(prompt)
        ai_response = clean_text(ai_response)
        store["messages"].append({"role": "ai", "content": ai_response})

        if user_id:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO chats (user_id, file_id, user_message, ai_response)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_id, file_id, user_message, ai_response)
                )
                conn.commit()
                cur.close()
                conn.close()
            except Exception as e:
                print(f"Warning: Could not save chat to DB: {e}")

        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": f"AI response could not be generated: {str(e)}"}), 500


@chat_bp.route("/history", methods=["GET"])
def history():
    store = _get_store()
    upload_store = _get_upload_store()

    return jsonify({
        "filename": upload_store.get("filename", ""),
        "messages": store.get("messages", [])
    })


@chat_bp.route("/reset", methods=["POST"])
def reset_chat():
    store = _get_store()
    store["messages"] = []
    return jsonify({"message": "Chat history cleared."})