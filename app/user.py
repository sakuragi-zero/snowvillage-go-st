"""
シンプルなユーザー管理
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import sqlite3
import os


@dataclass
class User:
    """ユーザーエンティティ"""
    id: Optional[int]
    username: str
    created_at: Optional[datetime] = None


class UserService:
    """ユーザーサービス"""
    
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'app_data', 'snowvillage.db')
        self._init_db()
    
    def _init_db(self):
        """データベース初期化"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def register_user(self, username: str) -> tuple[bool, str, Optional[User]]:
        """新規ユーザー登録"""
        if not username or not username.strip():
            return False, "名前を入力してください", None
        
        username = username.strip()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                # 既存ユーザーチェック
                existing = conn.execute(
                    "SELECT * FROM users WHERE username = ?", 
                    (username,)
                ).fetchone()
                
                if existing:
                    return False, "同じ名前のユーザーが既に存在します", None
                
                # 新規ユーザー作成
                cursor = conn.execute(
                    "INSERT INTO users (username) VALUES (?)",
                    (username,)
                )
                
                user_id = cursor.lastrowid
                user_data = conn.execute(
                    "SELECT * FROM users WHERE id = ?", 
                    (user_id,)
                ).fetchone()
                
                user = User(
                    id=user_data['id'],
                    username=user_data['username'],
                    created_at=datetime.fromisoformat(user_data['created_at'])
                )
                
                return True, "登録が完了しました！", user
                
        except Exception as e:
            return False, f"登録に失敗しました: {str(e)}", None
    
    def login_user(self, username: str) -> tuple[bool, str, Optional[User]]:
        """ユーザーログイン"""
        if not username or not username.strip():
            return False, "名前を入力してください", None
        
        username = username.strip()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                user_data = conn.execute(
                    "SELECT * FROM users WHERE username = ?", 
                    (username,)
                ).fetchone()
                
                if user_data:
                    user = User(
                        id=user_data['id'],
                        username=user_data['username'],
                        created_at=datetime.fromisoformat(user_data['created_at'])
                    )
                    return True, "ログインしました！", user
                else:
                    return False, "ユーザーが見つかりません", None
                    
        except Exception as e:
            return False, f"ログインに失敗しました: {str(e)}", None