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
        """データベースの初期化（新システムと互換性を持つ）"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    # ユーザーテーブル確認（既存テーブルがある場合は何もしない）
                    cursor.execute('''
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = 'users'
                        );
                    ''')
                    table_exists = cursor.fetchone()[0]
                    
                    if not table_exists:
                        # 新しいスキーマでテーブル作成（互換性のため）
                        cursor.execute('''
                            CREATE TABLE users (
                                id SERIAL PRIMARY KEY,
                                username VARCHAR(255) UNIQUE NOT NULL,
                                email VARCHAR(255) UNIQUE NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                last_login DATE,
                                streak INTEGER DEFAULT 0,
                                total_xp INTEGER DEFAULT 0,
                                daily_xp INTEGER DEFAULT 0,
                                gems INTEGER DEFAULT 50
                            )
                        ''')
                        conn.commit()
        except psycopg2.Error as e:
            print(f"Database initialization error: {e}")
            raise
    
    def check_user_exists(self, username: str) -> bool:
        """ユーザーが存在するかチェック"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute('SELECT COUNT(*) FROM users WHERE username = %s', [username])
                    count = cursor.fetchone()[0]
                    return count > 0
        except psycopg2.Error as e:
            print(f"Database error in check_user_exists: {e}")
            return False
    
    def register_user(self, username: str) -> Tuple[bool, str]:
        """新規ユーザー登録"""
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO users (username, email) VALUES (%s, %s)', 
                        [username, f"{username}@snowvillage.example"]
                    )
                    conn.commit()
                    return True, "登録が完了しました！"
        except psycopg2.IntegrityError:
            return False, "このユーザー名は既に登録されています"
        except psycopg2.Error as e:
            return False, f"登録中にエラーが発生しました: {e}"
    
    def login_user(self, username: str) -> Tuple[bool, str]:
        """既存ユーザーのログイン"""
        if self.check_user_exists(username):
            # 最終ログイン時間を更新
            try:
                with psycopg2.connect(**self.connection_params) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            'UPDATE users SET last_login = CURRENT_DATE WHERE username = %s',
                            [username]
                        )
                        conn.commit()
                return True, "ログインしました！"
            except psycopg2.Error as e:
                print(f"Database error in login_user: {e}")
                return False, f"ログイン更新中にエラーが発生しました: {e}"
        else:
            return False, "ユーザーが見つかりません"