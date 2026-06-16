"""SQLite database — stores completed analyses for result lookup."""

import json
import sqlite3
import os

DB_PATH = os.environ.get("DATABASE_URL", "critical_mineral.db")


def init_db():
    with _conn() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mineral_name TEXT NOT NULL,
                risk_json TEXT NOT NULL,
                asteroids_json TEXT NOT NULL,
                brief TEXT NOT NULL,
                demo_mode INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
        """)


def save_analysis(mineral_name: str, risk: dict, asteroids: list, brief: str, demo: bool) -> int:
    with _conn() as db:
        cur = db.execute(
            "INSERT INTO analyses (mineral_name, risk_json, asteroids_json, brief, demo_mode) VALUES (?,?,?,?,?)",
            (mineral_name, json.dumps(risk), json.dumps(asteroids), brief, 1 if demo else 0),
        )
        return cur.lastrowid


def get_analysis(analysis_id: int) -> dict | None:
    with _conn() as db:
        row = db.execute(
            "SELECT id, mineral_name, risk_json, asteroids_json, brief, demo_mode, created_at "
            "FROM analyses WHERE id=?",
            (analysis_id,),
        ).fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "mineral_name": row[1],
        "risk": json.loads(row[2]),
        "asteroids": json.loads(row[3]),
        "brief": row[4],
        "demo_mode": bool(row[5]),
        "created_at": row[6],
    }


def get_latest_by_mineral(mineral_name: str) -> dict | None:
    with _conn() as db:
        row = db.execute(
            "SELECT id, mineral_name, risk_json, asteroids_json, brief, demo_mode, created_at "
            "FROM analyses WHERE mineral_name=? ORDER BY id DESC LIMIT 1",
            (mineral_name.lower(),),
        ).fetchone()
    if not row:
        return None
    return {
        "id": row[0],
        "mineral_name": row[1],
        "risk": json.loads(row[2]),
        "asteroids": json.loads(row[3]),
        "brief": row[4],
        "demo_mode": bool(row[5]),
        "created_at": row[6],
    }


def list_analyses(limit: int = 20) -> list[dict]:
    with _conn() as db:
        rows = db.execute(
            "SELECT id, mineral_name, demo_mode, created_at FROM analyses ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [{"id": r[0], "mineral_name": r[1], "demo_mode": bool(r[2]), "created_at": r[3]} for r in rows]


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
