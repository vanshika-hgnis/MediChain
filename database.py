import sqlite3
from typing import Optional, List, Dict, Any
import json
import time


class Database:
    def __init__(self, db_name: str = "healthcare.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            )
            """
        )

        # Blocks table - using block_index instead of index (which is a SQL keyword)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS blocks (
                block_index INTEGER PRIMARY KEY,
                block_timestamp REAL NOT NULL,
                block_data TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                block_hash TEXT NOT NULL
            )
            """
        )

        # Medical records table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS medical_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                treatment TEXT NOT NULL,
                notes TEXT,
                record_date TEXT NOT NULL,
                block_index INTEGER,
                FOREIGN KEY (username) REFERENCES users (username),
                FOREIGN KEY (block_index) REFERENCES blocks (block_index)
            )
            """
        )

        # Access permissions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS access_permissions (
                patient_id TEXT NOT NULL,
                provider_id TEXT NOT NULL,
                grant_date TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES users (username),
                FOREIGN KEY (provider_id) REFERENCES users (username),
                PRIMARY KEY (patient_id, provider_id)
            )
            """
        )

        self.conn.commit()

    def add_user(self, username: str, password: str, user_type: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)",
                (username, password, user_type),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user(self, username: str) -> Optional[tuple]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

    def add_block(self, block) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO blocks (block_index, block_timestamp, block_data, previous_hash, block_hash)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    block.index,
                    block.timestamp,
                    json.dumps(block.data),
                    block.previous_hash,
                    block.hash,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_latest_block(self) -> Optional[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM blocks ORDER BY block_index DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            return {
                "index": row[0],
                "timestamp": row[1],
                "data": json.loads(row[2]),
                "previous_hash": row[3],
                "hash": row[4],
            }
        return None

    def add_medical_record(
        self, username: str, record_data: Dict[str, Any], block_index: int
    ) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO medical_records
                (username, diagnosis, treatment, notes, record_date, block_index)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    username,
                    record_data["diagnosis"],
                    record_data["treatment"],
                    record_data.get("notes", ""),
                    record_data["date"],
                    block_index,
                ),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_latest_block_index(self) -> Optional[int]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT block_index FROM blocks ORDER BY block_index DESC LIMIT 1"
        )
        row = cursor.fetchone()
        return row[0] if row else None

    def get_patient_records(self, username: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT m.*, b.block_hash 
            FROM medical_records m
            JOIN blocks b ON m.block_index = b.block_index
            WHERE m.username = ?
            ORDER BY m.record_date DESC
            """,
            (username,),
        )
        records = []
        for row in cursor.fetchall():
            records.append(
                {
                    "id": row[0],
                    "username": row[1],
                    "diagnosis": row[2],
                    "treatment": row[3],
                    "notes": row[4],
                    "date": row[5],
                    "block_index": row[6],
                    "block_hash": row[7],
                }
            )
        return records

    def add_access_permission(self, username: str, provider_id: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                INSERT INTO access_permissions (patient_id, provider_id, grant_date)
                VALUES (?, ?, ?)
                """,
                (username, provider_id, time.strftime("%Y-%m-%d %H:%M:%S")),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def check_access_permission(self, username: str, provider_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT 1 FROM access_permissions 
            WHERE patient_id = ? AND provider_id = ?
            """,
            (username, provider_id),
        )
        return cursor.fetchone() is not None

    def get_all_users(self) -> List[tuple]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT username, user_type FROM users")
        return cursor.fetchall()

    def close(self):
        self.conn.close()
