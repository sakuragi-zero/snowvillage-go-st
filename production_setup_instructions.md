# Snow Village Go - 本番データベース接続設定手順

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
