#!/usr/bin/env python3
"""
SQLiteからPostgreSQLにデータを移行するスクリプト
"""

import sqlite3
import psycopg2
import os
from datetime import datetime

def migrate_data():
    """SQLiteのデータをPostgreSQLに移行する"""
    
    # SQLiteデータベースファイルのパス
    sqlite_path = "app/app_data/snowvillage.db"
    
    # PostgreSQL接続パラメータ
    pg_params = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'snowvillage'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'port': os.getenv('DB_PORT', '5432')
    }
    
    if not os.path.exists(sqlite_path):
        print(f"SQLiteデータベースが見つかりません: {sqlite_path}")
        return False
    
    try:
        # SQLiteから既存データを読み取り
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_conn.row_factory = sqlite3.Row  # 辞書形式でアクセス可能
        sqlite_cursor = sqlite_conn.cursor()
        
        # usersテーブルのデータを取得
        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        print(f"SQLiteから{len(users)}件のユーザーデータを取得しました")
        
        # PostgreSQLに接続
        pg_conn = psycopg2.connect(**pg_params)
        pg_cursor = pg_conn.cursor()
        
        # PostgreSQLのテーブルを初期化（既存データをクリア）
        print("PostgreSQLのテーブルを初期化中...")
        pg_cursor.execute("DROP TABLE IF EXISTS users CASCADE")
        
        # テーブルを再作成
        pg_cursor.execute('''
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # データを移行
        migrated_count = 0
        for user in users:
            try:
                pg_cursor.execute(
                    '''INSERT INTO users (name, created_at, last_login) 
                       VALUES (%s, %s, %s)''',
                    (user['name'], user['created_at'], user['last_login'])
                )
                migrated_count += 1
            except psycopg2.IntegrityError as e:
                print(f"重複データをスキップ: {user['name']} - {e}")
                pg_conn.rollback()
        
        pg_conn.commit()
        print(f"PostgreSQLに{migrated_count}件のユーザーデータを移行しました")
        
        # 移行後の確認
        pg_cursor.execute("SELECT COUNT(*) FROM users")
        count = pg_cursor.fetchone()[0]
        print(f"PostgreSQL内のユーザー数: {count}")
        
        # 接続を閉じる
        sqlite_conn.close()
        pg_conn.close()
        
        print("データ移行が完了しました！")
        return True
        
    except sqlite3.Error as e:
        print(f"SQLiteエラー: {e}")
        return False
    except psycopg2.Error as e:
        print(f"PostgreSQLエラー: {e}")
        return False
    except Exception as e:
        print(f"予期しないエラー: {e}")
        return False

if __name__ == "__main__":
    print("SQLite -> PostgreSQL データ移行を開始します...")
    print(f"実行時刻: {datetime.now()}")
    
    success = migrate_data()
    
    if success:
        print("\n✅ データ移行が正常に完了しました")
    else:
        print("\n❌ データ移行中にエラーが発生しました")