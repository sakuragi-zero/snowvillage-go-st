# SnowVillage Docker環境 起動手順

## 前提条件
- Docker及びDocker Composeがインストールされていること

## 起動手順

### 1. PostgreSQLコンテナを起動
```bash
docker compose up -d db
```

### 2. データベースの準備完了を確認
```bash
docker compose logs db
```

### 3. 既存のSQLiteデータを移行（必要に応じて）
```bash
python migrate_sqlite_to_postgres.py
```

### 4. アプリケーションコンテナを起動
```bash
docker compose up -d app
```

### 5. 全サービスの起動確認
```bash
docker compose ps
```

### 6. アプリケーションへのアクセス
ブラウザで以下のURLにアクセス:
```
http://localhost:8501
```

## トラブルシューティング

### データベース接続エラーが発生する場合
1. PostgreSQLコンテナが正常に起動しているか確認
   ```bash
   docker compose logs db
   ```

2. 環境変数が正しく設定されているか確認
   ```bash
   docker compose exec app env | grep DB_
   ```

### 個別のコンテナを再起動したい場合
```bash
# データベースを再起動
docker compose restart db

# アプリケーションを再起動  
docker compose restart app
```

### ログを確認したい場合
```bash
# 全体のログを確認
docker compose logs

# 特定のサービスのログを確認
docker compose logs app
docker compose logs db
```

### 環境をクリーンアップしたい場合
```bash
# サービスを停止
docker compose down

# データも含めて完全にクリーンアップ
docker compose down -v
```