#!/usr/bin/env python3
"""
本番環境データベース接続テスト
Production Database Connection Test for Snow Village Go
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime


def test_production_connection():
    """本番環境データベース接続をテスト"""
    
    print("=" * 60)
    print("Snow Village Go - 本番環境データベース接続テスト")
    print("=" * 60)
    
    # 本番環境接続パラメータ
    prod_params = {
        'host': '160.16.58.221',
        'database': 'snowdb',
        'user': 'snowuser',
        'password': 'Snow-SWT2025-Village',
        'port': 5432,
        'sslmode': 'prefer',
        'connect_timeout': 10,
        'application_name': 'snowvillage_go_connection_test'
    }
    
    print(f"接続先: {prod_params['host']}:{prod_params['port']}")
    print(f"データベース: {prod_params['database']}")
    print(f"ユーザー: {prod_params['user']}")
    print("-" * 60)
    
    try:
        # 1. 基本接続テスト
        print("1. 基本接続テスト...")
        with psycopg2.connect(**prod_params) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version()")
                version = cur.fetchone()[0]
                print(f"   ✅ 接続成功: {version}")
        
        # 2. データベース情報取得
        print("\n2. データベース情報取得...")
        with psycopg2.connect(**prod_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # 現在時刻
                cur.execute("SELECT NOW() as current_time")
                result = cur.fetchone()
                print(f"   📅 サーバー時刻: {result['current_time']}")
                
                # データベースサイズ
                cur.execute("SELECT pg_size_pretty(pg_database_size(%s)) as db_size", (prod_params['database'],))
                result = cur.fetchone()
                print(f"   💾 データベースサイズ: {result['db_size']}")
        
        # 3. テーブル存在確認
        print("\n3. テーブル存在確認...")
        with psycopg2.connect(**prod_params) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name
                """)
                tables = cur.fetchall()
                
                if tables:
                    print("   📋 既存テーブル:")
                    for table in tables:
                        cur.execute(f"SELECT COUNT(*) FROM {table['table_name']}")
                        count = cur.fetchone()[0]
                        print(f"      - {table['table_name']}: {count} レコード")
                else:
                    print("   ℹ️  テーブルが存在しません（初回接続）")
        
        # 4. テーブル作成テスト
        print("\n4. テーブル作成テスト...")
        with psycopg2.connect(**prod_params) as conn:
            with conn.cursor() as cur:
                # usersテーブル作成
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # tasksテーブル作成
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        task_type TEXT DEFAULT 'basic',
                        description TEXT,
                        content JSONB
                    )
                """)
                
                # progressテーブル作成
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS progress (
                        id SERIAL PRIMARY KEY,
                        user_id INT NOT NULL,
                        task_id INT NOT NULL,
                        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (task_id) REFERENCES tasks(id),
                        UNIQUE(user_id, task_id)
                    )
                """)
                
                conn.commit()
                print("   ✅ テーブル作成/確認完了")
        
        # 5. 権限テスト
        print("\n5. データベース権限テスト...")
        with psycopg2.connect(**prod_params) as conn:
            with conn.cursor() as cur:
                # INSERT権限テスト
                try:
                    cur.execute("""
                        INSERT INTO users (username) 
                        VALUES ('connection_test_user') 
                        ON CONFLICT (username) DO NOTHING
                        RETURNING id
                    """)
                    result = cur.fetchone()
                    if result:
                        test_user_id = result[0]
                        print(f"   ✅ INSERT権限: OK (ユーザーID: {test_user_id})")
                    else:
                        print("   ✅ INSERT権限: OK (既存ユーザー)")
                    
                    # SELECT権限テスト
                    cur.execute("SELECT COUNT(*) FROM users")
                    user_count = cur.fetchone()[0]
                    print(f"   ✅ SELECT権限: OK (総ユーザー数: {user_count})")
                    
                    conn.commit()
                    
                except Exception as e:
                    print(f"   ❌ 権限エラー: {e}")
                    conn.rollback()
        
        # 6. 接続プール・同時接続テスト
        print("\n6. 同時接続テスト...")
        connections = []
        try:
            for i in range(3):
                conn = psycopg2.connect(**prod_params)
                connections.append(conn)
            print(f"   ✅ 同時接続: {len(connections)}個の接続を作成")
        except Exception as e:
            print(f"   ⚠️  同時接続制限: {e}")
        finally:
            for conn in connections:
                conn.close()
            print("   🔌 全ての接続を閉じました")
        
        print("\n" + "=" * 60)
        print("🎉 全てのテストが完了しました！")
        print("✅ 本番環境への接続準備が整いました")
        print("=" * 60)
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"\n❌ 接続エラー:")
        print(f"   {e}")
        print("\n🔧 確認事項:")
        print("   - サーバーが起動していますか？")
        print("   - ファイアウォール設定は正しいですか？")
        print("   - 接続情報（ホスト、ポート、認証情報）は正しいですか？")
        return False
        
    except psycopg2.DatabaseError as e:
        print(f"\n❌ データベースエラー:")
        print(f"   {e}")
        print("\n🔧 確認事項:")
        print("   - データベース名は正しいですか？")
        print("   - ユーザーに適切な権限がありますか？")
        return False
        
    except Exception as e:
        print(f"\n❌ 予期しないエラー:")
        print(f"   {e}")
        return False


def create_streamlit_secrets_template():
    """Streamlit Cloud用のsecrets.tomlテンプレート作成"""
    
    secrets_content = """# Streamlit Secrets Configuration for Production
# Add this configuration to your Streamlit Cloud app secrets

[database]
host = "160.16.58.221"
database = "snowdb"
user = "snowuser"
password = "Snow-SWT2025-Village"
port = 5432
sslmode = "prefer"
connect_timeout = 10

# Optional: Slack configuration
[slack]
bot_token = "xoxb-your-slack-bot-token"
channel_id = "C1234567890"
bot_name = "Snow Village Bot"
"""
    
    secrets_dir = os.path.join(os.path.dirname(__file__), ".streamlit")
    os.makedirs(secrets_dir, exist_ok=True)
    
    secrets_file = os.path.join(secrets_dir, "secrets_prod.toml")
    with open(secrets_file, "w", encoding="utf-8") as f:
        f.write(secrets_content)
    
    print(f"\n📝 本番環境用secrets設定ファイルを作成しました:")
    print(f"   {secrets_file}")
    print("\n⚠️  このファイルをStreamlit Cloudの秘密設定にコピーしてください")


if __name__ == "__main__":
    print("Snow Village Go - 本番環境データベース接続テスト")
    print("開始時刻:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    success = test_production_connection()
    
    if success:
        print("\n📋 次のステップ:")
        print("1. Streamlit CloudでSecretsを設定")
        print("2. アプリケーションをデプロイ")
        print("3. 本番環境でのテスト実行")
        
        # secrets.tomlテンプレート作成
        create_streamlit_secrets_template()
        
        sys.exit(0)
    else:
        print("\n❌ 接続テストが失敗しました")
        print("問題を解決してから再度実行してください")
        sys.exit(1)