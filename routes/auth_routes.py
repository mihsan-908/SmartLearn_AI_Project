from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from utils.db import get_db_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("auth.register"))

        if confirm_password and password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("auth.register"))

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return redirect(url_for("auth.register"))

        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM users WHERE username = %s OR email = %s",
                (username, email)
            )
            existing_user = cur.fetchone()

            if existing_user:
                flash("Username or email already exists.", "error")
                cur.close()
                return redirect(url_for("auth.register"))

            hashed_password = generate_password_hash(password)

            cur.execute(
                """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                """,
                (username, email, hashed_password)
            )
            conn.commit()
            cur.close()

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            if conn:
                conn.rollback()
            flash(f"Database error during registration: {str(e)}", "error")
            return redirect(url_for("auth.register"))
        finally:
            if conn:
                conn.close()

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for("auth.login"))

        conn = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT * FROM users WHERE username = %s OR email = %s",
                (username, username)
            )
            user = cur.fetchone()
            cur.close()

            if not user:
                flash("User not found.", "error")
                return redirect(url_for("auth.login"))

            if not check_password_hash(user["password_hash"], password):
                flash("Incorrect password.", "error")
                return redirect(url_for("auth.login"))

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("main.dashboard"))
        except Exception as e:
            flash(f"Database error during login: {str(e)}", "error")
            return redirect(url_for("auth.login"))
        finally:
            if conn:
                conn.close()

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("main.home"))