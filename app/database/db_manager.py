"""SQLiteデータベース管理システム"""

import sqlite3
import os
from pathlib import Path
from typing import Optional
import streamlit as st
from datetime import datetime


class DatabaseManager:
    """SQLiteデータベース管理クラス"""
    
    def __init__(self, db_path: str = "snowvillage.db"):
        """
        データベースマネージャーを初期化
        
        Args:
            db_path: データベースファイルのパス
        """
        self.db_path = db_path
        
        # データベースディレクトリを作成
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """データベース接続を取得"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 辞書のように行にアクセス可能
        return conn
    
    def init_database(self):
        """データベースとテーブルを初期化"""
        with self.get_connection() as conn:
            # usersテーブル作成
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    total_score INTEGER DEFAULT 0,
                    completed_challenges INTEGER DEFAULT 0
                )
            """)
            
            # challengesテーブル作成
            conn.execute("""
                CREATE TABLE IF NOT EXISTS challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT,
                    difficulty INTEGER DEFAULT 1,
                    question TEXT NOT NULL,
                    correct_answer TEXT NOT NULL,
                    options TEXT,  -- JSON形式で選択肢を保存
                    points INTEGER DEFAULT 10,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # user_progressテーブル作成
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    challenge_id INTEGER NOT NULL,
                    completed BOOLEAN DEFAULT FALSE,
                    score INTEGER DEFAULT 0,
                    attempts INTEGER DEFAULT 0,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (challenge_id) REFERENCES challenges (id),
                    UNIQUE(user_id, challenge_id)
                )
            """)
            
            # sessionsテーブル作成（セッション管理用）
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            conn.commit()
            print("✅ データベース初期化完了")
    
    def insert_sample_challenges(self):
        """サンプルチャレンジデータを挿入"""
        sample_challenges = [
            {
                'title': 'Snowflake基礎知識',
                'description': 'Snowflakeの基本概念について学びましょう',
                'category': 'basics',
                'difficulty': 1,
                'question': 'Snowflakeは何の種類のデータベースですか？',
                'correct_answer': 'クラウドデータウェアハウス',
                'options': '["クラウドデータウェアハウス", "NoSQLデータベース", "リレーショナルデータベース", "グラフデータベース"]',
                'points': 10
            },
            {
                'title': 'SQLクエリ基礎',
                'description': 'Snowflakeでの基本的なSQLクエリを学習',
                'category': 'sql',
                'difficulty': 2,
                'question': 'SELECT文でデータを並び替えるために使用するキーワードは？',
                'correct_answer': 'ORDER BY',
                'options': '["ORDER BY", "SORT BY", "ARRANGE BY", "GROUP BY"]',
                'points': 15
            },
            {
                'title': 'データローディング',
                'description': 'Snowflakeへのデータ読み込み方法',
                'category': 'loading',
                'difficulty': 3,
                'question': 'Snowflakeでファイルからデータを読み込むための主要な方法は？',
                'correct_answer': 'COPY INTO',
                'options': '["COPY INTO", "LOAD DATA", "INSERT FROM", "IMPORT FILE"]',
                'points': 20
            }
        ]
        
        with self.get_connection() as conn:
            for challenge in sample_challenges:
                try:
                    conn.execute("""
                        INSERT OR IGNORE INTO challenges 
                        (title, description, category, difficulty, question, correct_answer, options, points)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        challenge['title'],
                        challenge['description'],
                        challenge['category'],
                        challenge['difficulty'],
                        challenge['question'],
                        challenge['correct_answer'],
                        challenge['options'],
                        challenge['points']
                    ))
                except sqlite3.IntegrityError:
                    pass  # 既に存在する場合はスキップ
            
            conn.commit()
            print("✅ サンプルチャレンジデータ挿入完了")


# Streamlit用のデータベースインスタンス取得
@st.cache_resource
def get_db() -> DatabaseManager:
    """Streamlit用キャッシュされたデータベースインスタンスを取得"""
    db = DatabaseManager("app_data/snowvillage.db")
    
    # ディレクトリが存在しない場合は作成
    os.makedirs("app_data", exist_ok=True)
    
    # サンプルデータを挿入（初回のみ）
    db.insert_sample_challenges()
    
    return db