import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path("instance") / "niyaxvisuals.sqlite"
SCHEMA_PATH = Path("schema.sql")


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def seed_admin(username: str, password_hash: str) -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO admin_users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )


def get_admin_by_username(username: str):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM admin_users WHERE username = ?",
            (username,),
        ).fetchone()


def add_portfolio_item(
    title: str,
    category: str,
    description: str,
    image_filename: str,
    event_name: Optional[str] = None,
) -> None:
    created_at = datetime.utcnow().isoformat(timespec="seconds")
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO portfolio (created_at, title, category, event_name, description, image_filename)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (created_at, title, category, event_name, description, image_filename),
        )


def list_portfolio_items():
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM portfolio ORDER BY id DESC"
        ).fetchall()


def save_booking(
    name: str,
    email: str,
    shoot_type: str,
    video_style: Optional[str],
    message: str,
) -> None:
    created_at = datetime.utcnow().isoformat(timespec="seconds")
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO bookings (created_at, name, email, shoot_type, video_style, message)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (created_at, name, email, shoot_type, video_style, message),
        )


def list_bookings():
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM bookings ORDER BY id DESC"
        ).fetchall()