#!/usr/bin/env python3
"""
ネットワーク接続デバッグツール
Network Connection Debug Tool for Snow Village Go Production DB
"""

import socket
import subprocess
import sys
import os
from datetime import datetime


def test_network_connectivity():
    """ネットワーク接続をデバッグ"""
    
    host = "160.16.85.221"
    port = 5432
    
    print("=" * 60)
    print("Snow Village Go - ネットワーク接続デバッグ")
    print("=" * 60)
    print(f"対象サーバー: {host}:{port}")
    print(f"テスト時刻: {datetime.now()}")
    print("-" * 60)
    
    # 1. Pingテスト
    print("1. Pingテスト...")
    try:
        if os.name == 'nt':  # Windows
            result = subprocess.run(['ping', '-n', '4', host], 
                                 capture_output=True, text=True, timeout=30)
        else:  # Unix/Linux
            result = subprocess.run(['ping', '-c', '4', host], 
                                 capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("   ✅ Ping成功")
            # ping結果の要約を表示
            lines = result.stdout.strip().split('\n')
            for line in lines[-2:]:
                if line.strip():
                    print(f"      {line}")
        else:
            print("   ❌ Ping失敗")
            print(f"      {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("   ⏰ Pingタイムアウト")
    except Exception as e:
        print(f"   ❌ Pingエラー: {e}")
    
    # 2. ポート接続テスト
    print(f"\n2. ポート{port}接続テスト...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        
        if result == 0:
            print(f"   ✅ ポート{port}に接続成功")
        else:
            print(f"   ❌ ポート{port}への接続失敗 (エラーコード: {result})")
            
        sock.close()
        
    except socket.timeout:
        print(f"   ⏰ ポート{port}への接続タイムアウト")
    except Exception as e:
        print(f"   ❌ ポート接続エラー: {e}")
    
    # 3. DNS解決テスト
    print(f"\n3. DNS解決テスト...")
    try:
        ip_info = socket.gethostbyname_ex(host)
        print(f"   ✅ DNS解決成功")
        print(f"      ホスト名: {ip_info[0]}")
        print(f"      IPアドレス: {ip_info[2][0]}")
        
    except socket.gaierror as e:
        print(f"   ❌ DNS解決失敗: {e}")
    except Exception as e:
        print(f"   ❌ DNS解決エラー: {e}")
    
    # 4. トレースルート（可能な場合）
    print(f"\n4. 経路確認...")
    try:
        if os.name == 'nt':  # Windows
            cmd = ['tracert', '-h', '10', host]
        else:  # Unix/Linux
            cmd = ['traceroute', '-m', '10', host]
            
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("   ✅ 経路確認完了")
            # 最初と最後の数行のみ表示
            lines = result.stdout.strip().split('\n')
            for i, line in enumerate(lines):
                if i < 3 or i >= len(lines) - 2:
                    print(f"      {line}")
                elif i == 3:
                    print("      ...")
        else:
            print("   ⚠️  経路確認コマンド使用不可")
            
    except FileNotFoundError:
        print("   ℹ️  tracerouteコマンドが見つかりません")
    except subprocess.TimeoutExpired:
        print("   ⏰ 経路確認タイムアウト")
    except Exception as e:
        print(f"   ❌ 経路確認エラー: {e}")
    
    # 5. 環境情報
    print(f"\n5. 環境情報...")
    try:
        # 現在のIPアドレス確認
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        print(f"   🌐 ローカルIP: {local_ip}")
        
    except Exception as e:
        print(f"   ❌ ローカルIP取得エラー: {e}")
    
    # プラットフォーム情報
    import platform
    print(f"   💻 プラットフォーム: {platform.system()} {platform.release()}")
    print(f"   🐍 Python: {platform.python_version()}")
    
    # 推奨対処法
    print(f"\n" + "=" * 60)
    print("🔧 接続できない場合の対処法:")
    print("=" * 60)
    print("1. ファイアウォール設定:")
    print(f"   - サーバー側: ポート{port}への接続を許可")
    print(f"   - 送信元IP {local_ip if 'local_ip' in locals() else 'unknown'} を許可")
    print()
    print("2. PostgreSQL設定:")
    print("   - postgresql.conf: listen_addresses = '*'")
    print("   - pg_hba.conf: 適切なクライアント認証設定")
    print()
    print("3. ネットワーク設定:")
    print("   - VPN接続が必要な場合は接続を確認")
    print("   - プロキシ設定がある場合は迂回設定")
    print()
    print("4. Streamlit Cloud用設定:")
    print("   - Streamlit CloudのIPレンジを許可")
    print("   - SSL/TLS接続の有効化")


def create_connection_instructions():
    """接続設定手順書を作成"""
    
    instructions = """# Snow Village Go - 本番データベース接続設定手順

## 1. PostgreSQLサーバー設定

### postgresql.conf
```
listen_addresses = '*'
port = 5432
max_connections = 100
shared_buffers = 256MB
```

### pg_hba.conf
```
# Streamlit Cloud IP ranges (例)
host    snowdb    snowuser    0.0.0.0/0    md5

# より安全な設定（特定IPレンジのみ）
host    snowdb    snowuser    YOUR_IP_RANGE/24    md5
```

## 2. ファイアウォール設定

### Ubuntu/CentOS
```bash
# ポート5432を開放
sudo ufw allow 5432/tcp
# または
sudo firewall-cmd --permanent --add-port=5432/tcp
sudo firewall-cmd --reload
```

### AWS Security Group
```
Type: PostgreSQL
Protocol: TCP
Port: 5432
Source: 0.0.0.0/0 (または特定IP)
```

## 3. PostgreSQL再起動
```bash
sudo systemctl restart postgresql
```

## 4. 接続テスト
```bash
psql -h 160.16.58.221 -U snowuser -d snowdb
```

## 5. Streamlit Cloud設定
```toml
[database]
host = "160.16.58.221"
database = "snowdb"
user = "snowuser"
password = "Snow-SWT2025-Village"
port = 5432
sslmode = "prefer"
connect_timeout = 10
```
"""
    
    with open("production_setup_instructions.md", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print(f"📚 設定手順書を作成しました: production_setup_instructions.md")


if __name__ == "__main__":
    test_network_connectivity()
    create_connection_instructions()
    
    print(f"\n⏰ テスト完了時刻: {datetime.now()}")
    print("\n次のステップ:")
    print("1. 上記の対処法を実行")
    print("2. db_connection_test_prod.py を再実行") 
    print("3. 接続成功後にStreamlit Cloudにデプロイ")