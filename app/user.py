"""
シンプルなユーザー管理
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import psycopg2
import psycopg2.extras
import os
import streamlit as st


@dataclass
class User:
    """ユーザーエンティティ"""
    id: Optional[int]
    username: str
    created_at: Optional[datetime] = None


class UserService:
    """ユーザーサービス"""
    
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
        """データベース初期化"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with psycopg2.connect(**self.connection_params) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users (
                                id SERIAL PRIMARY KEY,
                                username VARCHAR(50) UNIQUE NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """)
                        conn.commit()
                    print(f"Database connection successful (attempt {attempt + 1})")
                    return
            except psycopg2.OperationalError as e:
                print(f"Database connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to connect to database after {max_retries} attempts: {e}")
            except Exception as e:
                print(f"Database initialization error: {e}")
                if attempt == max_retries - 1:
                    raise
    
    def register_user(self, username: str) -> tuple[bool, str, Optional[User]]:
        """新規ユーザー登録"""
        if not username or not username.strip():
            return False, "名前を入力してください", None
        
        username = username.strip()
        
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    # 既存ユーザーチェック
                    cursor.execute(
                        "SELECT * FROM users WHERE username = %s", 
                        (username,)
                    )
                    existing = cursor.fetchone()
                    
                    if existing:
                        return False, "同じ名前のユーザーが既に存在します", None
                    
                    # 新規ユーザー作成
                    cursor.execute(
                        "INSERT INTO users (username) VALUES (%s) RETURNING *",
                        (username,)
                    )
                    user_data = cursor.fetchone()
                    
                    user = User(
                        id=user_data['id'],
                        username=user_data['username'],
                        created_at=user_data['created_at']
                    )
                    
                    conn.commit()
                    return True, "登録が完了しました！", user
                    
        except Exception as e:
            return False, f"登録に失敗しました: {str(e)}", None
    
    def login_user(self, username: str) -> tuple[bool, str, Optional[User]]:
        """ユーザーログイン"""
        if not username or not username.strip():
            return False, "名前を入力してください", None
        
        username = username.strip()
        
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    cursor.execute(
                        "SELECT * FROM users WHERE username = %s", 
                        (username,)
                    )
                    user_data = cursor.fetchone()
                    
                    if user_data:
                        user = User(
                            id=user_data['id'],
                            username=user_data['username'],
                            created_at=user_data['created_at']
                        )
                        return True, "ログインしました！", user
                    else:
                        return False, "ユーザーが見つかりません", None
                        
        except Exception as e:
            return False, f"ログインに失敗しました: {str(e)}", None