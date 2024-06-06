import sqlite3
import os
import utils
from typing import Optional, List, Dict
from config import cfg


class SQLiteDBAdapter:
    def __init__(self):
        self.db_path = utils.escape_chars(f"{cfg['dbPath']}\{cfg['dbName']}")
        self._schema_init()
        self.params = self.Params(self)
        self.sessions = self.Sessions(self)

    def _schema_init(self):
        self._create_dbfile()
        self._create_params_table()
        self._create_session_table()
        self._create_batches_table()
        self._create_runs_table()
        self._create_nodes_table()
        self._create_node_data_table()

    def _create_dbfile(self):
        if not os.path.exists(self.db_path):
            open(self.db_path, "w").close()

    def _create_params_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS params (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value TEXT NOT NULL
                )
            """
            )
            conn.commit()

    def _create_session_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name VARCHAR(255) NOT NULL,
                    session_script VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
            conn.commit()

    def _create_batches_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS batches (
                    batch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INT REFERENCES sessions(session_id),
                    param_id INT REFERENCES params_table(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
            conn.commit()

    def _create_runs_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS runs (
                run_id INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id INT REFERENCES batches(batch_id),
                run_number INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
            conn.commit()

    def _create_nodes_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS nodes (
                node_id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_name VARCHAR(255) NOT NULL,
                ip_address VARCHAR(45) NOT NULL 
                );
            """
            )
            conn.commit()

    def _create_node_data_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS node_data (
                    data_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id INT REFERENCES runs(run_id),
                    node_id INT REFERENCES nodes(node_id),
                    data JSONB NOT NULL,
                    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
            conn.commit()

    class Params:
        def __init__(self, adapter):
            self.adapter = adapter

        def insert_setting(self, value: str) -> Dict[str, int | str]:
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO params (value) VALUES (?)", (value,))
                conn.commit()
                new_id = cursor.lastrowid
                return {"id": int(new_id), "value": value}

        def get_setting(self, id: int) -> Optional[Dict[str, int]]:
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, value FROM params WHERE id = ?", (id,))
                row = cursor.fetchone()
                return {"id": int(row[0]), "value": row[1]} if row else None

        def update_setting(self, id: int, value: str) -> bool:
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE params SET value = ? WHERE id = ?", (value, id))
                conn.commit()
                return cursor.rowcount > 0

        def delete_setting(self, id: int) -> bool:
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM params WHERE id = ?", (id,))
                conn.commit()
                return cursor.rowcount > 0

        def get_all_settings(self) -> List[Dict[str | int, str]]:
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, value FROM params")
                rows = cursor.fetchall()
                return [{"id": int(row[0]), "value": row[1]} for row in rows]

    class Sessions:

        def __init__(self, adapter):
            self.adapter = adapter

        def insert_session(
            self, session_name: str, session_script: str
        ) -> Dict[str, int | str]:
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                INSERT INTO sessions (session_name, session_script) VALUES (?, ?)
                                """,
                    (session_name, session_script),
                )
                conn.commit()
                new_id = cursor.lastrowid
                return {
                    "id": int(new_id),
                    "sessionName": session_name,
                    "sessonScript": session_script,
                }

        def get_all_sessions(self) -> List[Dict[str, int | str]]:
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT session_id, session_name, session_script FROM sessions"
                )
                rows = cursor.fetchall()
                return [
                    dict(session_id=row[0], session_name=row[1], session_script=row[2])
                    for row in rows
                ]
