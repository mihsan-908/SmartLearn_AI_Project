from flask import Blueprint, render_template, session, redirect, url_for
from utils.db import get_db_connection

main_bp = Blueprint("main", __name__)


def login_required():
    return "user_id" in session


@main_bp.route("/")
def home():
    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("auth.login"))

    user_id = session.get("user_id")
    stats = {
        "uploads": 0,
        "chats": 0,
        "quizzes": 0,
        "summaries": 0,
        "notes": 0
    }

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) as count FROM uploaded_files WHERE user_id = %s", (user_id,))
        stats["uploads"] = cur.fetchone()["count"]

        cur.execute("SELECT COUNT(*) as count FROM chats WHERE user_id = %s", (user_id,))
        stats["chats"] = cur.fetchone()["count"]

        cur.execute("SELECT COUNT(*) as count FROM quizzes WHERE user_id = %s", (user_id,))
        stats["quizzes"] = cur.fetchone()["count"]

        cur.execute("SELECT COUNT(*) as count FROM summaries WHERE user_id = %s", (user_id,))
        stats["summaries"] = cur.fetchone()["count"]

        cur.execute("SELECT COUNT(*) as count FROM notes WHERE user_id = %s", (user_id,))
        stats["notes"] = cur.fetchone()["count"]

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not load user dashboard stats: {e}")

    return render_template("dashboard/dashboard.html", stats=stats)


@main_bp.route("/history")
def history():
    if not login_required():
        return redirect(url_for("auth.login"))

    user_id = session.get("user_id")
    summaries = []
    quizzes = []
    notes = []
    chats = []

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM summaries WHERE user_id = %s ORDER BY created_at DESC LIMIT 20", (user_id,))
        summaries = cur.fetchall()

        cur.execute("SELECT * FROM quizzes WHERE user_id = %s ORDER BY created_at DESC LIMIT 20", (user_id,))
        quizzes = cur.fetchall()

        cur.execute("SELECT * FROM notes WHERE user_id = %s ORDER BY created_at DESC LIMIT 20", (user_id,))
        notes = cur.fetchall()

        cur.execute("SELECT * FROM chats WHERE user_id = %s ORDER BY created_at DESC LIMIT 20", (user_id,))
        chats = cur.fetchall()

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Warning: Could not load history: {e}")

    return render_template(
        "dashboard/history.html",
        summaries=summaries,
        quizzes=quizzes,
        notes=notes,
        chats=chats
    )


@main_bp.route("/about")
def about():
    return render_template("about.html")


@main_bp.route("/features")
def features():
    return render_template("features.html")


@main_bp.route("/contact")
def contact():
    return render_template("contact.html")