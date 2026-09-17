import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app


def get_db_connection():
    conn = psycopg2.connect(
        host=current_app.config["DB_HOST"],
        database=current_app.config["DB_NAME"],
        user=current_app.config["DB_USER"],
        password=current_app.config["DB_PASSWORD"],
        port=current_app.config["DB_PORT"],
        cursor_factory=RealDictCursor
    )
    return conn


def init_db():
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database", "schema.sql")
    if os.path.exists(schema_path):
        conn = get_db_connection()
        cur = conn.cursor()
        with open(schema_path, "r", encoding="utf-8") as f:
            cur.execute(f.read())
        conn.commit()
        cur.close()
        conn.close()