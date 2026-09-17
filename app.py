from flask import Flask
from dotenv import load_dotenv
import os

from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.chat_routes import chat_bp
from routes.upload_routes import upload_bp
from routes.summary_routes import summary_bp
from routes.quiz_routes import quiz_bp
from routes.notes_routes import notes_bp

load_dotenv()

app = Flask(__name__)

# Core settings
app.secret_key = os.getenv("SECRET_KEY", "smartlearn_ai_secret")
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "static/uploads")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload

# PostgreSQL settings from .env
app.config["DB_HOST"] = os.getenv("DB_HOST", "localhost")
app.config["DB_NAME"] = os.getenv("DB_NAME", "SmartLearn-AI")
app.config["DB_USER"] = os.getenv("DB_USER", "postgres")
app.config["DB_PASSWORD"] = os.getenv("DB_PASSWORD")
app.config["DB_PORT"] = os.getenv("DB_PORT", "5432")

# Make sure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(upload_bp, url_prefix="/upload")
app.register_blueprint(summary_bp, url_prefix="/summary")
app.register_blueprint(quiz_bp, url_prefix="/quiz")
app.register_blueprint(notes_bp, url_prefix="/notes")

with app.app_context():
    try:
        from utils.db import init_db
        init_db()
    except Exception as e:
        print(f"Notice: Database auto-init skipped or failed: {e}")

if __name__ == "__main__":
    app.run(debug=True)