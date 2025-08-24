import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import streamlit as st

class TaskService:
    """タスクサービス"""
    def __init__(self):
        # Streamlit Cloud環境での接続パラメータ
        try:
            # Streamlit Secretsから接続情報を取得
            db_config = st.secrets.get("database", {})
            self.connection_params = {
                'host': db_config.get('host', os.getenv('DB_HOST', 'デフォルト')),
                'database': db_config.get('database', os.getenv('DB_NAME', 'snowvillage')),
                'user': db_config.get('user', os.getenv('DB_USER', 'postgres')),
                'password': db_config.get('password', os.getenv('DB_PASSWORD', '')),
                'port': int(db_config.get('port', os.getenv('DB_PORT', '5432'))),
                # 外部インスタンス接続用のSSL設定
                'sslmode': db_config.get('sslmode', 'prefer'),
                'connect_timeout': int(db_config.get('connect_timeout', '10')),
                'application_name': 'snowvillage_go_app'
            }
        except Exception as e:
            # Secretsが利用できない場合（ローカル開発環境）
            print(f"Using fallback database configuration: {e}")
            self.connection_params = {
                'host': os.getenv('DB_HOST', 'postgres-dev'),
                'database': os.getenv('DB_NAME', 'snowvillage'),
                'user': os.getenv('DB_USER', 'postgres'),
                'password': os.getenv('DB_PASSWORD', 'devpassword'),
                'port': int(os.getenv('DB_PORT', '5432')),
                'sslmode': 'prefer',
                'connect_timeout': 10,
                'application_name': 'snowvillage_go_app'
            }
        self._init_db()

    def _init_db(self):
        """テーブル初期化"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
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
                            id SERIAL PRIMARY KEY,
                            user_id INT NOT NULL,
                            task_id INT NOT NULL,
                            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (task_id) REFERENCES tasks(id),
                            UNIQUE(user_id, task_id)
                        )
                        """)
                    conn.commit()
                    print(f"Task database connection successful (attempt {attempt + 1})")
                    return
            except psycopg2.OperationalError as e:
                print(f"Task database connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to connect to task database after {max_retries} attempts: {e}")
            except Exception as e:
                print(f"Task database initialization error: {e}")
                if attempt == max_retries - 1:
                    raise

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

    def mark_task_complete(self, task_id: int, user_id: int):
        """タスクを完了にマーク"""
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO progress (user_id, task_id, completed_at)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id, task_id)
                    DO UPDATE SET completed_at = EXCLUDED.completed_at
                """, (user_id, task_id, datetime.now()))
            conn.commit()

    def get_tasks_with_progress(self, user_id: int):
        """タスクと進捗を取得"""
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT t.id, t.title, t.task_type, t.description, t.content,
                        CASE WHEN p.task_id IS NOT NULL THEN TRUE ELSE FALSE END AS completed
                    FROM tasks t
                    LEFT JOIN progress p ON t.id = p.task_id AND p.user_id = %s
                    ORDER BY t.id
                """, (user_id,))
                return cur.fetchall()

    def get_user_ranking(self):
        """ユーザーのタスク完了数ランキングを取得（上位10位）"""
        with psycopg2.connect(**self.connection_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT u.username, 
                           COUNT(p.task_id) as completed_tasks,
                           MAX(p.completed_at) as last_completion
                    FROM users u
                    LEFT JOIN progress p ON u.id = p.user_id
                    GROUP BY u.id, u.username
                    ORDER BY completed_tasks DESC, last_completion ASC NULLS LAST
                    LIMIT 10
                """)
                return cur.fetchall()
