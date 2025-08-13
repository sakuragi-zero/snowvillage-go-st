import psycopg2
import psycopg2.extras
import os
from contextlib import contextmanager
from typing import Generator, Dict, Any


class DatabaseConnection:
    """データベース接続クラス"""
    
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'postgres-dev'),
            'database': os.getenv('DB_NAME', 'snowvillage'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'devpassword'),
            'port': int(os.getenv('DB_PORT', '5432'))
        }
    
    @contextmanager
    def get_connection(self) -> Generator[psycopg2.extensions.connection, None, None]:
        """データベース接続のコンテキストマネージャー"""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    @contextmanager
    def get_cursor(self) -> Generator[psycopg2.extensions.cursor, None, None]:
        """カーソルのコンテキストマネージャー"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try:
                yield cursor
            finally:
                cursor.close()
    
    def create_tables(self) -> None:
        """テーブル作成"""
        with self.get_cursor() as cursor:
            # ユーザーテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login DATE,
                    streak INTEGER DEFAULT 0,
                    total_xp INTEGER DEFAULT 0,
                    daily_xp INTEGER DEFAULT 0,
                    gems INTEGER DEFAULT 50
                )
            """)
            
            # ミッションテーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS missions (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(100) NOT NULL,
                    icon VARCHAR(10) NOT NULL,
                    description TEXT NOT NULL,
                    lessons INTEGER NOT NULL,
                    xp_reward INTEGER NOT NULL,
                    gem_reward INTEGER NOT NULL,
                    order_index INTEGER DEFAULT 0
                )
            """)
            
            # ミッション進捗テーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    mission_id INTEGER REFERENCES missions(id) ON DELETE CASCADE,
                    completed_lessons INTEGER DEFAULT 0,
                    is_completed BOOLEAN DEFAULT FALSE,
                    completed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, mission_id)
                )
            """)
            
            # タスク進捗テーブル
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_progress (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    task_id INTEGER NOT NULL,
                    mission_id INTEGER NOT NULL,
                    is_completed BOOLEAN DEFAULT FALSE,
                    completed_at TIMESTAMP,
                    answer_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, task_id)
                )
            """)
            
            # 更新トリガー
            cursor.execute("""
                CREATE OR REPLACE FUNCTION update_updated_at_column()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ language 'plpgsql';
            """)
            
            cursor.execute("""
                DROP TRIGGER IF EXISTS update_progress_updated_at ON progress;
                CREATE TRIGGER update_progress_updated_at
                    BEFORE UPDATE ON progress
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at_column();
            """)
            
            cursor.execute("""
                DROP TRIGGER IF EXISTS update_task_progress_updated_at ON task_progress;
                CREATE TRIGGER update_task_progress_updated_at
                    BEFORE UPDATE ON task_progress
                    FOR EACH ROW
                    EXECUTE FUNCTION update_updated_at_column();
            """)


# グローバルインスタンス
db = DatabaseConnection()