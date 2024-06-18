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
        self.batches = self.Batches(self)
        self.nodes = self.Nodes(self)
        self.runs = self.Runs(self)
        self.node_data = self.Node_data(self)
        self.analysis = self.Analysis(self)
        self.batch_results = self.Batch_results(self)
        self.session_results = self.Session_results(self)
        self.dataPasser = self.DataPasser(self)

    def _schema_init(self):
        self._create_dbfile()
        self._create_params_table()
        self._create_session_table()
        self._create_batches_table()
        self._create_runs_table()
        self._create_nodes_table()
        self._create_node_data_table()
        self._create_batch_result_table()
        self._create_session_results_table()
        self._create_data_passing_table()

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
                session_id INTEGER NOT NULL,
                param_used TEXT NOT NULL,
                number_of_nodes INTEGER NOT NULL DEFAULT 0,  
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            );
            """
            )
            conn.commit()

    def _create_batch_result_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS batch_result (
                    batch_id INTEGER REFERENCES batches(batch_id),
                    standard_deviation DECIMAL,
                    mean_execution_time DECIMAL,
                    path_to_graph VARCHAR(255),
                    PRIMARY KEY (batch_id),
                    FOREIGN KEY (batch_id) REFERENCES batches(batch_id)
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
                node_name TEXT NOT NULL,
                ip_address TEXT NOT NULL,
                UNIQUE(node_name, ip_address)
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
                    execution_output TEXT,
                    execution_time DECIMAL,
                    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
            conn.commit()

    def _create_session_results_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions_results (
                    session_result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INT REFERENCES sessions(session_id),
                    result_path_mean VARCHAR(255) NOT NULL,
                    result_path_std_dev VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """
            )
            conn.commit()

    def _create_data_passing_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS data_passer (
                    key_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_name VARCHAR(255) UNIQUE NOT NULL,
                    value VARCHAR(255) NOT NULL
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
                    "session_id": int(new_id),
                    "session_name": session_name,
                    "session_script": session_script,
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

    class Batches:

        def __init__(self, adapter):
            self.adapter = adapter

        def create_new_batch(self, session_id, param_used, number_of_nodes):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO batches (session_id, param_used, number_of_nodes)
                    VALUES (?, ?, ?);
                    """,
                    (session_id, param_used, number_of_nodes),
                )
                conn.commit()
                return cursor.lastrowid

        def get_param_used_by_batch_id(self, batch_id):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT param_used FROM batches WHERE batch_id = ?;
                    """,
                    (batch_id,),
                )
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return ""

    class Nodes:
        def __init__(self, adapter):
            self.adapter = adapter

        def create_new_node(self, node_name, ip_address):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO nodes (node_name, ip_address)
                    VALUES (?, ?)
                    ON CONFLICT(node_name, ip_address) DO NOTHING;
                    """,
                    (node_name, ip_address),
                )
                if cursor.lastrowid == 0:  # No new row was inserted due to conflict
                    cursor.execute(
                        """
                        SELECT node_id FROM nodes WHERE node_name = ? AND ip_address = ?;
                        """,
                        (node_name, ip_address),
                    )
                    existing_node = cursor.fetchone()
                    return existing_node[0] if existing_node else None

                conn.commit()
                return cursor.lastrowid

        def get_node_id(self, node_name, ip_address):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT node_id FROM nodes WHERE node_name = ? AND ip_address = ?;
                    """,
                    (node_name, ip_address),
                )
                node = cursor.fetchone()
                return node[0] if node else None

    class Runs:

        def __init__(self, adapter):
            self.adapter = adapter

        def create_new_run(self, batch_id, run_number):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO runs (batch_id, run_number)
                    VALUES (?, ?);
                    """,
                    (batch_id, run_number),
                )
                conn.commit()
                return cursor.lastrowid

    class Node_data:

        def __init__(self, adapter):
            self.adapter = adapter

        def create_node_data(self, run_id, node_id, execution_output, execution_time):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO node_data (run_id, node_id, execution_output, execution_time)
                    VALUES (?, ?, ?, ?);
                    """,
                    (run_id, node_id, execution_output, execution_time),
                )
                conn.commit()
                return cursor.lastrowid

    class Batch_results:
        def __init__(self, adapter):
            self.adapter = adapter

        def insert_batch_result(
            self, batch_id, standard_deviation, mean_execution_time, path_to_graph, unit
        ):
            try:
                with sqlite3.connect(self.adapter.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO batch_result (batch_id, standard_deviation, mean_execution_time, path_to_graph,unit)
                        VALUES (?, ?, ?, ?)
                    """,
                        (
                            batch_id,
                            standard_deviation,
                            mean_execution_time,
                            path_to_graph,
                            unit,
                        ),
                    )
                    conn.commit()
                    return cursor.lastrowid
            except sqlite3.Error as e:
                print("Error occurred:", e)
                return None

        def reset_batch_results_for_session(self, session_id):
            try:
                with sqlite3.connect(self.adapter.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        DELETE FROM batch_result
                        WHERE batch_id IN (
                            SELECT batch_id
                            FROM batches
                            WHERE session_id = ?
                        )
                    """,
                        (session_id,),
                    )
                    conn.commit()
            except sqlite3.Error as e:
                print("Error occurred:", e)

        def get_batch_results_for_session(self, session_id):
            batch_results = []
            try:
                with sqlite3.connect(self.adapter.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        SELECT batches.batch_id, batches.param_used, batch_result.standard_deviation, 
                            batch_result.mean_execution_time, batch_result.path_to_graph
                        FROM batches
                        JOIN batch_result ON batches.batch_id = batch_result.batch_id
                        WHERE batches.session_id = ?
                    """,
                        (session_id,),
                    )
                    rows = cursor.fetchall()
                    for row in rows:
                        batch_results.append(
                            {
                                "batch_id": row[0],
                                "param_used": row[1],
                                "standard_deviation": row[2],
                                "mean_execution_time": row[3],
                                "path_to_graph": row[4],
                            }
                        )
            except sqlite3.Error as e:
                print("Error occurred:", e)
            return batch_results

    class Session_results:

        def __init__(self, adapter):
            self.adapter = adapter

        def insert_session_result(self, session_id, path_to_mean, path_to_std_dev):
            try:
                with sqlite3.connect(self.adapter.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO sessions_results (session_id, result_path_mean, result_path_std_dev)
                        VALUES (?, ?, ?)
                        """,
                        (session_id, path_to_mean, path_to_std_dev),
                    )
                    conn.commit()
            except sqlite3.Error as e:
                print("Error occurred:", e)

        def reset_session_results(self, session_id):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM sessions_results WHERE session_id = ?;", (session_id,)
                )
                conn.commit()

        def get_session_result_paths(self, session_id):
            try:
                with sqlite3.connect(self.adapter.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        SELECT result_path_mean, result_path_std_dev
                        FROM sessions_results
                        WHERE session_id = ?
                        """,
                        (session_id,),
                    )
                    result = cursor.fetchone()
                    if result:
                        result_path_mean, result_path_std_dev = result
                        return result_path_mean, result_path_std_dev
                    else:
                        print("No result found for session ID:", session_id)
                        return None, None
            except sqlite3.Error as e:
                print("Error occurred:", e)
                return None, None

    class Analysis:

        def __init__(self, adapter):
            self.adapter = adapter

        def get_detailed_combined_data(self):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT
                        s.session_name,
                        s.session_script,
                        b.batch_id AS batch_number,
                        b.param_used,
                        b.number_of_nodes,
                        r.run_number,
                        nd.execution_time
                    FROM
                        sessions s
                        JOIN batches b ON s.session_id = b.session_id
                        JOIN runs r ON b.batch_id = r.batch_id
                        JOIN node_data nd ON r.run_id = nd.run_id
                        JOIN (
                            SELECT
                                run_id,
                                MAX(execution_time) AS max_execution_time
                            FROM
                                node_data
                            GROUP BY
                                run_id
                        ) nd_max ON nd.run_id = nd_max.run_id AND nd.execution_time = nd_max.max_execution_time
                    ORDER BY
                        s.session_name, b.number_of_nodes, r.run_number;
                    """
                )
                rows = cursor.fetchall()
                return rows

        def get_session_batches_with_times(self, session_id):
            session_batches = []
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT batches.batch_id, batches.param_used, GROUP_CONCAT(max_execution_times.max_execution_time) as batch_times
                    FROM batches
                    LEFT JOIN runs ON batches.batch_id = runs.batch_id
                    LEFT JOIN (
                        SELECT run_id, MAX(execution_time) AS max_execution_time
                        FROM node_data
                        GROUP BY run_id
                    ) max_execution_times ON runs.run_id = max_execution_times.run_id
                    WHERE batches.session_id = ?
                    GROUP BY batches.batch_id, batches.param_used
                    """,
                    (session_id,),
                )
                rows = cursor.fetchall()
                for row in rows:
                    batch_id, param_used, batch_times = row
                    session_batches.append(
                        {
                            "batch_id": batch_id,
                            "param_used": param_used,
                            "batch_times": (
                                list(map(float, batch_times.split(",")))
                                if batch_times
                                else []
                            ),
                        }
                    )
            return session_batches

        def get_session_batches(self, session_id):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT b.batch_id, br.mean_execution_time, br.standard_deviation, b.number_of_nodes
                    FROM batches b
                    JOIN batch_result br ON b.batch_id = br.batch_id
                    WHERE b.session_id = ?
                    """,
                    (session_id,),
                )
                batches = []
                for row in cursor.fetchall():
                    batch_info = {
                        "batch_id": row[0],
                        "batch_mean_time": row[1],
                        "batch_std_deviation": row[2],
                        "batch_number_of_nodes": row[3],
                    }
                    batches.append(batch_info)
                return batches

    class DataPasser:
        def __init__(self, adapter):
            self.adapter = adapter

        def store(self, key_name, value):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO data_passer (key_name, value)
                    VALUES (?, ?)
                    ON CONFLICT(key_name) DO UPDATE SET
                        value=excluded.value
                    """,
                    (key_name, value),
                )
                conn.commit()

        def retrieve(self, key_name):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT value FROM data_passer WHERE key_name = ?", (key_name,)
                )
                result = cursor.fetchone()
                return result[0] if result else None

        def exists(self, key_name):
            with sqlite3.connect(self.adapter.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT 1 FROM data_passer WHERE key_name = ?", (key_name,)
                )
                result = cursor.fetchone()
                return result is not None
