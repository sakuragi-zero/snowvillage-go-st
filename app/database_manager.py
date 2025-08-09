"""
データベース管理モジュール
ユーザー情報の管理を行います
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import Optional, Tuple

class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'snowvillage'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password'),
            'port': os.getenv('DB_PORT', '5432')
        }
        self.init_database()
    
    def init_database(self):
        """データベースの初期化"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    # ユーザーテーブルの作成
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255) UNIQUE NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    ''')
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Database initialization error: {e}")
            raise
    
    def check_user_exists(self, name: str) -> bool:
        """ユーザーが存在するかチェック"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT COUNT(*) FROM users WHERE name = %s', (name,))
                    count = cursor.fetchone()[0]
                    return count > 0
        except psycopg2.Error as e:
            print(f"Database error in check_user_exists: {e}")
            return False
    
    def register_user(self, name: str) -> Tuple[bool, str]:
        """新規ユーザー登録"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO users (name) VALUES (%s)', 
                        (name,)
                    )
                    conn.commit()
                    return True, "登録が完了しました！"
        except psycopg2.IntegrityError:
            return False, "このユーザー名は既に登録されています"
        except psycopg2.Error as e:
            return False, f"登録中にエラーが発生しました: {e}"
    
    def login_user(self, name: str) -> Tuple[bool, str]:
        """既存ユーザーのログイン"""
        if self.check_user_exists(name):
            # 最終ログイン時間を更新
            try:
                with psycopg2.connect(**self.connection_params) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE name = %s',
                            (name,)
                        )
                        conn.commit()
                return True, "ログインしました！"
            except psycopg2.Error as e:
                print(f"Database error in login_user: {e}")
                return False, f"ログイン更新中にエラーが発生しました: {e}"
        else:
            return False, "ユーザーが見つかりません"