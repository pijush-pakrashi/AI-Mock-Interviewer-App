"""Elevate AI - Persistent Interview History & Revision Manager.

Uses SQLite to persist candidate mock interview sessions, questions, answers,
scores, and reports across browser sessions for continuous revision.
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional


class HistoryManager:
    """Handles database storage and retrieval for candidate mock interviews."""

    def __init__(self, db_path: str = "data/elevate_history.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes SQLite schema if not already present."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS interview_sessions (
                    session_id TEXT PRIMARY KEY,
                    candidate_name TEXT NOT NULL,
                    candidate_email TEXT,
                    candidate_degree TEXT,
                    candidate_branch TEXT,
                    candidate_stage TEXT,
                    role TEXT NOT NULL,
                    company TEXT,
                    difficulty TEXT,
                    overall_score REAL,
                    total_questions INTEGER,
                    qas_json TEXT NOT NULL,
                    final_report TEXT,
                    study_materials TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_session(
        self,
        candidate_profile: Dict[str, Any],
        role: str,
        company: str,
        difficulty: str,
        qas: List[Dict[str, Any]],
        final_report: Optional[str] = None,
        study_materials: Optional[str] = None,
        overall_score: float = 0.0
    ) -> str:
        """Saves a completed mock interview session to the database."""
        session_id = str(uuid.uuid4())
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO interview_sessions (
                    session_id, candidate_name, candidate_email, candidate_degree,
                    candidate_branch, candidate_stage, role, company, difficulty,
                    overall_score, total_questions, qas_json, final_report,
                    study_materials, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    candidate_profile.get("name", "Candidate"),
                    candidate_profile.get("email", ""),
                    candidate_profile.get("degree", ""),
                    candidate_profile.get("branch", ""),
                    candidate_profile.get("stage", ""),
                    role,
                    company or "General Tech",
                    difficulty,
                    overall_score,
                    len(qas),
                    json.dumps(qas, ensure_ascii=False),
                    final_report or "",
                    study_materials or "",
                    created_at
                )
            )
            conn.commit()
        return session_id

    def get_candidate_sessions(self, email_or_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves past sessions for a specific candidate or all recent sessions."""
        with self._get_connection() as conn:
            if email_or_name:
                cursor = conn.execute(
                    """
                    SELECT * FROM interview_sessions 
                    WHERE candidate_email = ? OR candidate_name = ?
                    ORDER BY created_at DESC
                    """,
                    (email_or_name, email_or_name)
                )
            else:
                cursor = conn.execute(
                    "SELECT * FROM interview_sessions ORDER BY created_at DESC"
                )
            
            rows = cursor.fetchall()
            results = []
            for row in rows:
                item = dict(row)
                try:
                    item["qas"] = json.loads(item["qas_json"])
                except Exception:
                    item["qas"] = []
                results.append(item)
            return results

    def get_session_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single interview session by session ID."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM interview_sessions WHERE session_id = ?",
                (session_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            item = dict(row)
            try:
                item["qas"] = json.loads(item["qas_json"])
            except Exception:
                item["qas"] = []
            return item

    def delete_session(self, session_id: str) -> bool:
        """Deletes a session from history."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM interview_sessions WHERE session_id = ?",
                (session_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
