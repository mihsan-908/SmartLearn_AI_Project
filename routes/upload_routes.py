from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import uuid

from utils.pdf_extractor import extract_text
from utils.helpers import allowed_file, ensure_folder, clean_text, truncate_text
from utils.db import get_db_connection

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "static/uploads"

# Shared in-memory store for current uploaded PDF per browser session
pdf_text_storage = {}


def _get_client_id():
    if "client_id" not in session:
        session["client_id"] = str(uuid.uuid4())
    return session["client_id"]


def _get_store():
    client_id = _get_client_id()
    if client_id not in pdf_text_storage:
        pdf_text_storage[client_id] = {
            "file_id": None,
            "filename": "",
            "path": "",
            "text": ""
        }
        # If user is logged in, try restoring their latest uploaded file from DB
        user_id = session.get("user_id")
        if user_id:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT id, file_name, extracted_text 
                    FROM uploaded_files 
                    WHERE user_id = %s 
                    ORDER BY upload_date DESC LIMIT 1
                    """,
                    (user_id,)
                )
                latest = cur.fetchone()
                cur.close()
                conn.close()
                if latest:
                    pdf_text_storage[client_id]["file_id"] = latest["id"]
                    pdf_text_storage[client_id]["filename"] = latest["file_name"]
                    pdf_text_storage[client_id]["text"] = latest["extracted_text"]
            except Exception:
                pass
    return pdf_text_storage[client_id]


@upload_bp.route("/", methods=["GET", "POST"])
def upload():
    if "user_id" not in session:
        if request.method == "POST":
            return jsonify({"error": "Please log in first to upload documents."}), 401
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        store = _get_store()
        return render_template("dashboard/upload.html", filename=store.get("filename", ""))

    if "file" not in request.files:
        return jsonify({"error": "No file selected."}), 400

    file = request.files["file"]

    if not file or file.filename == "":
        return jsonify({"error": "Please choose a PDF file."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files are allowed."}), 400

    ensure_folder(UPLOAD_FOLDER)

    safe_name = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, safe_name)
    file.save(save_path)
    file_size = os.path.getsize(save_path) if os.path.exists(save_path) else 0

    extracted_text = extract_text(save_path)
    extracted_text = truncate_text(clean_text(extracted_text), 15000)

    file_id = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO uploaded_files (user_id, file_name, original_name, file_size, extracted_text)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (session["user_id"], safe_name, file.filename, file_size, extracted_text)
        )
        row = cur.fetchone()
        if row:
            file_id = row["id"]
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not save upload to DB: {e}")

    store = _get_store()
    store["file_id"] = file_id
    store["filename"] = safe_name
    store["path"] = save_path
    store["text"] = extracted_text

    return jsonify({
        "message": "PDF uploaded successfully.",
        "filename": safe_name,
        "file_id": file_id,
        "text_length": len(extracted_text)
    })


@upload_bp.route("/text", methods=["GET"])
def uploaded_text():
    store = _get_store()
    return jsonify({
        "file_id": store.get("file_id"),
        "filename": store.get("filename", ""),
        "text": store.get("text", "")
    })


@upload_bp.route("/clear", methods=["POST"])
def clear_upload():
    store = _get_store()
    store["file_id"] = None
    store["filename"] = ""
    store["path"] = ""
    store["text"] = ""

    return jsonify({"message": "Uploaded file cleared."})