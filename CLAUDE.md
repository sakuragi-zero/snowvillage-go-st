# Snow Village Go Project - Development Knowledge Base

このファイルは、Snow Village Goプロジェクトの開発に関する重要な情報とトラブルシューティングガイドを記載しています。

## データベース設定

### 接続設定の統一
すべてのサービス（UserService、TaskService等）は同じデータベース接続設定を使用する必要があります。

**標準設定:**
```python
self.connection_params = {
    'host': os.getenv('DB_HOST', 'postgres-dev'),
    'database': os.getenv('DB_NAME', 'snowvillage'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'devpassword'),
    'port': int(os.getenv('DB_PORT', '5432'))
}
```

### 環境変数での上書き
本番環境や開発環境に応じて、以下の環境変数で設定を上書きできます：

- `DB_HOST`: データベースホスト（デフォルト: postgres-dev）
- `DB_NAME`: データベース名（デフォルト: snowvillage）
- `DB_USER`: ユーザー名（デフォルト: postgres）
- `DB_PASSWORD`: パスワード（デフォルト: devpassword）
- `DB_PORT`: ポート番号（デフォルト: 5432）

### Docker環境での接続
- **開発環境**: `docker-compose.dev.yml`を使用（postgres-dev コンテナ、デフォルト設定）
- **本番環境**: `docker-compose.yml`を使用（snowvillage-postgres コンテナ、パスワード: password）
- **重要**: 環境変数を設定しない場合、デフォルトで`postgres-dev`コンテナに接続される

## タスク管理システム

### 自動テーブル作成
`TaskService`の初期化時に以下のテーブルが自動作成されます：

1. **tasks テーブル**
   ```sql
   CREATE TABLE IF NOT EXISTS tasks (
       id SERIAL PRIMARY KEY,
       title TEXT NOT NULL
   );
   ```

2. **progress テーブル**
   ```sql
   CREATE TABLE IF NOT EXISTS progress (
       task_id INT PRIMARY KEY,
       completed_at TIMESTAMP,
       FOREIGN KEY (task_id) REFERENCES tasks(id)
   );
   ```

### タスクタイプシステム（v2.0）
- **2種類のミッション**: 技術クイズ系（quiz）とSNS投稿系（sns）
- **拡張されたデータベーススキーマ**: 
  - `task_type`: タスクの種類（quiz/sns/basic）
  - `description`: タスクの説明
  - `content`: クイズ問題やSNS投稿要件（JSONB形式）

### 折りたたみ式UI
- **ページ階層なし**: 全てのタスクをダッシュボード内で完結
- **クイズ機能**: 4択問題、即座のフィードバック、正解時に自動完了
- **SNS投稿機能**: ブース訪問要件、投稿プロンプト、完了ボタン
- **ボタン反応性**: ユニークキー設定、session_state管理で安定動作

### YAMLファイルからのタスク同期
- `tasks.yml`ファイルからタスクを自動読み込み
- 拡張フォーマット対応（type, description, content）
- アプリケーション起動時に`sync_yaml_to_db()`でデータベースに同期

**クイズタスクフォーマット例:**
```yaml
- id: 1
  title: "データ取得技術"
  type: "quiz"
  description: "データベースからのデータ取得に関する技術クイズです"
  content:
    question: "SQLでテーブルの全てのレコードを取得するコマンドは？"
    options:
      - "SELECT * FROM table_name"
      - "GET ALL FROM table_name"
    correct_answer: 0
```

**SNSタスクフォーマット例:**
```yaml
- id: 2
  title: "AI・MLブースを訪問"
  type: "sns"
  description: "AI・MLブースを訪問してSNSに投稿しよう！"
  content:
    booth_name: "AI・MLテクノロジーブース"
    sns_prompt: "AI・MLブースで最新技術を体験中！ #SnowVillage"
    requirements:
      - "ブーススタッフと写真を撮る"
      - "ハッシュタグ #SnowVillage を含める"
```

## よくあるトラブル

### 1. データベース接続エラー
**症状**: `psycopg2.OperationalError: connection to server failed`

**原因と解決策**:
- PostgreSQLコンテナが起動していない → `docker compose up -d`で起動
- 接続設定が間違っている → 環境変数やデフォルト値を確認
- パスワードが間違っている → docker-compose.ymlで設定したパスワードを確認

### 2. テーブルが存在しないエラー
**症状**: `psycopg2.errors.UndefinedColumn: column p.task_id does not exist`

**原因と解決策**:
- **データベース接続先の違い**: 複数のPostgreSQLコンテナが存在する場合、接続先によってテーブル構成が異なる
- **解決法**: 
  - **デフォルト接続（推奨）**: 環境変数なしで`postgres-dev`コンテナに接続
    ```bash
    uv run streamlit run main.py
    ```
  - **localhost接続**: 必要に応じて環境変数で`localhost`に接続
    ```bash
    export DB_HOST=localhost DB_PASSWORD=password
    uv run streamlit run main.py
    ```
- `TaskService`が正しく初期化されていない → インスタンス作成時のエラーログを確認
- 手動でテーブル作成は不要 → `_init_db()`メソッドが自動実行される

### 3. 依存関係エラー
**症状**: `ImportError`や`ModuleNotFoundError`

**解決策**:
```bash
uv sync --reinstall
```

## ファイル構成

### コア機能
- `user.py`: ユーザー認証・管理システム
- `task_db.py`: タスク管理データベース操作
- `tasks.py`: YAMLファイルとの同期機能
- `main.py`: アプリケーションエントリーポイント
- `launch_screen.py`: ログイン画面
- `pages/dashboard.py`: メインダッシュボード

### 設定ファイル
- `tasks.yml`: タスク定義ファイル
- `pyproject.toml`: Python依存関係設定
- `docker-compose.yml`: 本番環境コンテナ設定
- `docker-compose.dev.yml`: 開発環境コンテナ設定

## 開発時の注意点

1. **新しいサービス作成時**: 必ず`user.py`の`UserService`と同じ接続設定を使用する
2. **データベーススキーマ変更時**: `_init_db()`メソッドを更新する
3. **環境変数**: 本番環境では適切な環境変数を設定する
4. **依存関係**: 新しいライブラリ追加時は`pyproject.toml`を更新する

## テスト・デバッグ

### データベース接続テスト
```bash
uv run python -c "from task_db import TaskService; ts = TaskService(); print('OK')"
```

### テーブル確認
```bash
docker exec snowvillage-postgres psql -U postgres -d snowvillage -c "\\dt"
```

### アプリケーション起動
**デフォルト設定で起動（推奨）:**
```bash
uv run streamlit run main.py
```
※ postgres-devコンテナに接続され、usersテーブルとタスクデータが利用可能

**localhost接続で起動:**
```bash
export DB_HOST=localhost DB_PASSWORD=password
uv run streamlit run main.py
```
※ snowvillage-postgresコンテナに接続（必要に応じて使用）