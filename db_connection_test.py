#!/usr/bin/env python3
"""
データベース疎通確認スクリプト
PostgreSQLデータベースへの接続とテーブルのクエリを実行します
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

def get_db_connection_params():
    """環境変数またはデフォルト値からDB接続パラメータを取得"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'snowvillage'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'port': os.getenv('DB_PORT', '5432')
    }

def test_database_connection():
    """データベース接続テスト"""
    print("=== データベース疎通確認 ===")
    print(f"テスト開始時刻: {datetime.now()}")
    
    connection_params = get_db_connection_params()
    print(f"接続先: {connection_params['host']}:{connection_params['port']}")
    print(f"データベース: {connection_params['database']}")
    print(f"ユーザー: {connection_params['user']}")
    print("-" * 40)
    
    try:
        # データベース接続テスト
        print("1. データベース接続テスト...")
        with psycopg2.connect(**connection_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                
                # PostgreSQLバージョン確認
                cursor.execute("SELECT version();")
                version = cursor.fetchone()
                print(f"   ✓ 接続成功")
                print(f"   PostgreSQLバージョン: {version['version']}")
                
                # 現在の日時取得
                cursor.execute("SELECT CURRENT_TIMESTAMP as current_time;")
                current_time = cursor.fetchone()
                print(f"   データベース現在時刻: {current_time['current_time']}")
                print()
                
                # テーブル一覧確認
                print("2. テーブル一覧確認...")
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name;
                """)
                tables = cursor.fetchall()
                
                if tables:
                    print(f"   ✓ 検出されたテーブル数: {len(tables)}")
                    for table in tables:
                        print(f"   - {table['table_name']}")
                else:
                    print("   ⚠ テーブルが見つかりませんでした")
                print()
                
                # usersテーブルが存在する場合の詳細確認
                if any(table['table_name'] == 'users' for table in tables):
                    print("3. usersテーブル詳細確認...")
                    
                    # テーブル構造確認
                    cursor.execute("""
                        SELECT column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns 
                        WHERE table_name = 'users' 
                        ORDER BY ordinal_position;
                    """)
                    columns = cursor.fetchall()
                    
                    print("   テーブル構造:")
                    for col in columns:
                        nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                        default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
                        print(f"   - {col['column_name']}: {col['data_type']} {nullable}{default}")
                    
                    # レコード数確認
                    cursor.execute("SELECT COUNT(*) as count FROM users;")
                    count = cursor.fetchone()
                    print(f"   ✓ 登録ユーザー数: {count['count']}")
                    
                    # 最新の登録ユーザー確認（レコードがある場合）
                    if count['count'] > 0:
                        cursor.execute("""
                            SELECT name, created_at, last_login 
                            FROM users 
                            ORDER BY created_at DESC 
                            LIMIT 5;
                        """)
                        recent_users = cursor.fetchall()
                        print("   最新の登録ユーザー（最大5件）:")
                        for user in recent_users:
                            print(f"   - {user['name']} (登録: {user['created_at']}, 最終ログイン: {user['last_login']})")
                    print()
                
                print("4. データベース統計情報...")
                # データベースサイズ
                cursor.execute("""
                    SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;
                """)
                db_size = cursor.fetchone()
                print(f"   データベースサイズ: {db_size['db_size']}")
                
                # アクティブな接続数
                cursor.execute("""
                    SELECT count(*) as active_connections
                    FROM pg_stat_activity 
                    WHERE state = 'active';
                """)
                connections = cursor.fetchone()
                print(f"   アクティブ接続数: {connections['active_connections']}")
                
    except psycopg2.OperationalError as e:
        print(f"   ✗ 接続エラー: {e}")
        print("   データベースサーバーが起動しているか確認してください")
        return False
        
    except psycopg2.Error as e:
        print(f"   ✗ データベースエラー: {e}")
        return False
        
    except Exception as e:
        print(f"   ✗ 予期しないエラー: {e}")
        return False
    
    print("-" * 40)
    print("✓ データベース疎通確認が完了しました")
    print(f"テスト終了時刻: {datetime.now()}")
    return True

if __name__ == "__main__":
    success = test_database_connection()
    exit(0 if success else 1)