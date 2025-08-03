"""
データベース管理モジュール
ユーザー情報の管理を行います
"""

import sqlite3
import os
from typing import Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "app_data/snowvillage.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """データベースの初期化"""
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # ユーザーテーブルの作成
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def check_user_exists(self, name: str) -> bool:
        """ユーザーが存在するかチェック"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM users WHERE name = ?', (name,))
            count = cursor.fetchone()[0]
            return count > 0
    
    def register_user(self, name: str) -> Tuple[bool, str]:
        """新規ユーザー登録"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (name) VALUES (?)', 
                    (name,)
                )
                conn.commit()
                return True, "登録が完了しました！"
        except sqlite3.IntegrityError:
            return False, "このユーザー名は既に登録されています"
        except Exception as e:
            return False, f"登録中にエラーが発生しました: {e}"
    
    def login_user(self, name: str) -> Tuple[bool, str]:
        """既存ユーザーのログイン"""
        if self.check_user_exists(name):
            # 最終ログイン時間を更新
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE name = ?',
                    (name,)
                )
                conn.commit()
            return True, "ログインしました！"
        else:
            return False, "ユーザーが見つかりません"