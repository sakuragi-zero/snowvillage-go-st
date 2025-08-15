import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

class TaskService:
    """タスクサービス"""
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'postgres-dev'),
            'database': os.getenv('DB_NAME', 'snowvillage'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'devpassword'),
            'port': int(os.getenv('DB_PORT', '5432'))
        }
        self._init_db()

    def _init_db(self):
        """テーブル初期化"""
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    task_type TEXT DEFAULT 'basic',
                    description TEXT,
                    content JSONB
                )
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress (
                    task_id INT PRIMARY KEY,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks(id)
                )
                """)
            conn.commit()

    def insert_task_if_not_exists(self, task_id: int, title: str, task_type: str = 'basic', description: str = None, content: dict = None):
        """タスクがなければ追加"""
        import json
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM tasks WHERE id = %s", (task_id,))
                if not cur.fetchone():
                    content_json = json.dumps(content) if content else None
                    cur.execute("""
                        INSERT INTO tasks (id, title, task_type, description, content) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (task_id, title, task_type, description, content_json))
            conn.commit()

    def mark_task_complete(self, task_id: int):
        """タスクを完了にマーク"""
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO progress (task_id, completed_at)
                    VALUES (%s, %s)
                    ON CONFLICT (task_id)
                    DO UPDATE SET completed_at = EXCLUDED.completed_at
                """, (task_id, datetime.now()))
            conn.commit()

    def get_tasks_with_progress(self):
        """タスクと進捗を取得"""
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT t.id, t.title, t.task_type, t.description, t.content,
                        CASE WHEN p.task_id IS NOT NULL THEN TRUE ELSE FALSE END AS completed
                    FROM tasks t
                    LEFT JOIN progress p ON t.id = p.task_id
                    ORDER BY t.id
                """)
                return cur.fetchall()
