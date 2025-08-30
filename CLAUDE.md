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

## パフォーマンス最適化（2025年8月実装）

### 実装背景
投稿ボタンやページ遷移の度に以下の問題が発生していた：
- `TaskService`初期化時に毎回CREATE TABLE文が実行される
- YAMLからのタスク同期で重複チェッククエリが大量発生
- PostgreSQLの直列処理により数ms〜数十msの遅延が積み重なる

### 最適化策

#### 1. グローバル初期化フラグ機能
```python
# task_db.py
_DB_INITIALIZED = False
_TASKS_SYNCED = False

def _ensure_db_initialized(self):
    global _DB_INITIALIZED
    if _DB_INITIALIZED:
        return
    # 初回のみ実行
```

**効果**: 
- 初回: 0.423秒 → 2回目以降: 0.000秒（∞倍高速化）
- CREATE TABLE文の重複実行を完全排除

#### 2. Streamlitセッション状態キャッシング
```python
# セッション状態での二重チェック
if hasattr(st.session_state, '_db_initialized') and st.session_state._db_initialized:
    _DB_INITIALIZED = True
    return
```

**効果**: ページ遷移時も初期化をスキップ

#### 3. 一括挿入機能（bulk_insert_tasks_if_not_exists）
```python
# 既存：個別にSELECT + INSERT
for task in tasks:
    cur.execute("SELECT 1 FROM tasks WHERE id = %s", (task_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO tasks...")

# 最適化：一括SELECT + 一括INSERT
cur.execute(f"SELECT id FROM tasks WHERE id IN ({format_strings})", task_ids)
existing_ids = set(row[0] for row in cur.fetchall())
cur.executemany("INSERT INTO tasks...", new_tasks_data)
```

**効果**: 
- 個別挿入: 0.022秒 → 一括挿入: 0.002秒（11倍高速化）
- 90個タスク同期: 0.052秒 → 2回目以降: 0.000秒

#### 4. タスク同期の最適化
```python
# tasks.py
def sync_yaml_to_db(yaml_path: str):
    if _TASKS_SYNCED or (hasattr(st.session_state, '_tasks_synced') and st.session_state._tasks_synced):
        return  # 同期済みの場合は即座に終了
    
    task_service.bulk_insert_tasks_if_not_exists(tasks)  # 一括処理
    st.session_state._tasks_synced = True  # フラグ設定
```

### パフォーマンステスト結果

| 処理 | 最適化前 | 最適化後 | 改善率 |
|------|---------|----------|--------|
| DB初期化（2回目） | 0.423秒 | 0.000秒 | ∞倍 |
| タスク同期（2回目） | 0.052秒 | 0.000秒 | ∞倍 |
| 一括vs個別挿入 | 0.022秒 | 0.002秒 | 11倍 |
| 複数インスタンス作成 | 各0.4秒 | 各0.000秒 | ∞倍 |

### 運用上の注意点

1. **フラグリセット**: アプリケーション再起動時に自動でリセットされる
2. **メモリ使用量**: グローバルフラグは最小限のメモリ使用量
3. **デバッグ時**: `performance_test.py`で動作確認可能
4. **本番環境**: Streamlit Cloudでも同様の効果を確認

### ファイル構成
- `task_db.py`: 初期化フラグとバルク挿入機能
- `tasks.py`: 同期最適化ロジック  
- `performance_test.py`: 性能測定スクリプト

## 開発時の注意点

1. **新しいサービス作成時**: 必ず`user.py`の`UserService`と同じ接続設定を使用する
2. **データベーススキーマ変更時**: `_init_db()`メソッドを更新する
3. **パフォーマンス重視**: 初期化処理は`_ensure_db_initialized()`パターンを使用する
4. **大量データ処理**: 個別処理ではなく一括処理（`bulk_*`メソッド）を優先する
5. **環境変数**: 本番環境では適切な環境変数を設定する
6. **依存関係**: 新しいライブラリ追加時は`pyproject.toml`を更新する

## Streamlit Cloud デプロイメント

### 必要な設定

1. **Streamlit Secrets設定**
   - Streamlit Cloudの管理画面でSecretsを設定
   - `.streamlit/secrets.toml.example`を参考に以下の設定を追加:

```toml
[database]
host = "your-external-postgres-host.com"
database = "snowvillage"
user = "your_db_user"
password = "your_secure_password"
port = 5432
sslmode = "require"
connect_timeout = 10

[slack]
bot_token = "xoxb-your-slack-bot-token"
channel_id = "C1234567890"
bot_name = "Snow Village Bot"
```

2. **データベース要件**
   - PostgreSQL 12以上
   - SSL接続対応（推奨: sslmode=require）
   - ファイアウォール設定でStreamlit Cloud IPからのアクセスを許可
   - タイムゾーン設定: UTC推奨

3. **接続設定**
   - **SSL必須**: 外部インスタンス接続時はSSL設定必須
   - **接続プール**: アプリケーション名による識別
   - **タイムアウト**: 10秒のタイムアウト設定
   - **リトライ**: 3回の接続リトライ機能

### デプロイメント手順

1. GitHubリポジトリにpush
2. Streamlit Cloudでアプリを作成
3. Secretsに接続情報を設定
4. デプロイ実行
5. ログでデータベース接続成功を確認

## テスト・デバッグ

### データベース接続テスト

**ローカル環境（Docker）:**
```bash
uv run python -c "from task_db import TaskService; ts = TaskService(); print('OK')"
```

**Streamlit Cloud環境:**
- Streamlit Cloud上でアプリを起動し、ログを確認
- 接続成功時は "Database connection successful" メッセージが表示される

### テーブル確認

**ローカル環境:**
```bash
docker exec snowvillage-postgres psql -U postgres -d snowvillage -c "\\dt"
```

**外部PostgreSQL:**
```bash
psql -h your-host -p 5432 -U your-user -d snowvillage -c "\\dt"
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

## UI開発での重要な注意点

### ボタンキーの重複エラー
- **問題**: `StreamlitDuplicateElementKey` エラー - 同じキーのボタンが複数存在
- **原因**: 複数の表示関数で同じキー形式を使用（例：`close_sns_{task_id}`）
- **解決**: 
  - ボタンキーに機能別の接尾辞を追加（例：`close_sns_content_{task_id}`）
  - 重複する古い関数を削除
  - セッション状態キーの統一（`show_quiz_{task_id}`, `show_sns_{task_id}`）

### ボタンをHTMLカード内に配置しない
- **問題**: HTMLカード内のボタンは反応しない
- **解決**: 必ずStreamlitボタンをカード外に配置
- **ベストプラクティス**: `st.columns()`でレイアウト調整