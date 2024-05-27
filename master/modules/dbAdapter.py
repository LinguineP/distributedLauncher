import sqlite3
import os
import utils
from typing import Optional, List, Dict
from config import cfg


class SQLiteDBAdapter:
    def __init__(self):
        self.db_path = utils.escape_chars(f"{cfg['dbPath']}\{cfg['dbName']}")
        self._create_dbfile()
        self._create_params_table()

    def _create_dbfile(self):
        if not os.path.exists(self.db_path):
            open(self.db_path, "w").close()

    def _create_params_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS params_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value TEXT NOT NULL
                )
            """
            )
            conn.commit()

    def insert_params_setting(self, value: str) -> Dict[int, str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO params_table (value) VALUES (?)", (value,))
            conn.commit()
            new_id = cursor.lastrowid
            return {"id": int(new_id), "value": value}

    def get_params_setting(self, id: int) -> Optional[Dict[int, str]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, value FROM params_table WHERE id = ?", (id,))
            row = cursor.fetchone()
            return {"id": int(row[0]), "value": row[1]} if row else None

    def update_params_setting(self, id: int, value: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE params_table SET value = ? WHERE id = ?", (value, id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_params_setting(self, id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM params_table WHERE id = ?", (id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_all_params_settings(self) -> List[Dict[int, str]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, value FROM params_table")
            rows = cursor.fetchall()
            return [{"id": int(row[0]), "value": row[1]} for row in rows]
