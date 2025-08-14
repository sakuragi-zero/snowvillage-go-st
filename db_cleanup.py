#!/usr/bin/env python3
"""
データベースクリーンアップスクリプト
usersテーブル以外の全てのテーブルを削除します
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


def get_db_connection_params():
    """環境変数またはデフォルト値からDB接続パラメータを取得"""
    return {
        'host': os.getenv('DB_HOST', 'postgres-dev'),
        'database': os.getenv('DB_NAME', 'snowvillage'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'devpassword'),
        'port': int(os.getenv('DB_PORT', '5432'))
    }


def cleanup_database():
    """usersテーブル以外の全てのテーブルを削除"""
    print("=== データベースクリーンアップ ===")
    print(f"実行開始時刻: {datetime.now()}")
    
    connection_params = get_db_connection_params()
    print(f"接続先: {connection_params['host']}:{connection_params['port']}")
    print(f"データベース: {connection_params['database']}")
    print(f"ユーザー: {connection_params['user']}")
    print("-" * 50)
    
    try:
        with psycopg2.connect(**connection_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                
                # 現在のテーブル一覧を取得
                print("1. 現在のテーブル一覧を確認...")
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_name;
                """)
                all_tables = cursor.fetchall()
                
                if not all_tables:
                    print("   ⚠ テーブルが見つかりませんでした")
                    return True
                
                print(f"   ✓ 検出されたテーブル数: {len(all_tables)}")
                for table in all_tables:
                    print(f"   - {table['table_name']}")
                print()
                
                # usersテーブル以外を特定
                tables_to_delete = [
                    table['table_name'] for table in all_tables 
                    if table['table_name'] != 'users'
                ]
                
                if not tables_to_delete:
                    print("2. 削除対象のテーブルなし")
                    print("   ✓ usersテーブル以外のテーブルは存在しません")
                    return True
                
                print(f"2. 削除対象のテーブル（{len(tables_to_delete)}個）:")
                for table_name in tables_to_delete:
                    print(f"   - {table_name}")
                print()
                
                # 確認プロンプト
                print("⚠ 警告: 上記のテーブルとそのデータは完全に削除されます！")
                while True:
                    confirm = input("削除を実行しますか? (yes/no): ").lower().strip()
                    if confirm in ['yes', 'y']:
                        break
                    elif confirm in ['no', 'n']:
                        print("削除をキャンセルしました")
                        return False
                    else:
                        print("'yes' または 'no' で答えてください")
                
                print()
                print("3. テーブル削除を実行中...")
                
                # 外部キー制約を一時的に無効化
                cursor.execute("SET session_replication_role = replica;")
                
                deleted_count = 0
                for table_name in tables_to_delete:
                    try:
                        print(f"   削除中: {table_name}")
                        cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
                        deleted_count += 1
                        print(f"   ✓ 削除完了: {table_name}")
                    except Exception as e:
                        print(f"   ✗ 削除失敗: {table_name} - {e}")
                
                # 外部キー制約を有効化
                cursor.execute("SET session_replication_role = DEFAULT;")
                
                # 変更をコミット
                conn.commit()
                
                print()
                print(f"4. 削除結果: {deleted_count}/{len(tables_to_delete)} テーブル削除")
                
                # 削除後のテーブル一覧確認
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_type = 'BASE TABLE'
                    ORDER BY table_name;
                """)
                remaining_tables = cursor.fetchall()
                
                print("5. 削除後のテーブル一覧:")
                if remaining_tables:
                    for table in remaining_tables:
                        print(f"   - {table['table_name']}")
                else:
                    print("   すべてのテーブルが削除されました")
                
    except psycopg2.OperationalError as e:
        print(f"   ✗ 接続エラー: {e}")
        print("   データベースサーバーが起動しているか確認してください")
        return False
        
    except psycopg2.Error as e:
        print(f"   ✗ データベースエラー: {e}")
        return False
        
    except KeyboardInterrupt:
        print("\n   ✗ ユーザーによる中断")
        return False
        
    except Exception as e:
        print(f"   ✗ 予期しないエラー: {e}")
        return False
    
    print("-" * 50)
    print("✓ データベースクリーンアップが完了しました")
    print(f"実行終了時刻: {datetime.now()}")
    return True


if __name__ == "__main__":
    success = cleanup_database()
    exit(0 if success else 1)