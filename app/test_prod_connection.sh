#!/bin/bash

# Snow Village Go - 本番環境データベース接続テスト実行スクリプト

echo "=================================================="
echo "Snow Village Go - 本番環境データベース接続テスト"
echo "=================================================="
echo

# 環境変数設定（オプション）
export PGHOST=160.16.58.221
export PGUSER=snowuser  
export PGPASSWORD=Snow-SWT2025-Village
export PGDATABASE=snowdb

# Python仮想環境の確認
if command -v uv &> /dev/null; then
    echo "🚀 uvを使用して接続テストを実行..."
    uv run python db_connection_test_prod.py
elif [ -f "venv/bin/activate" ]; then
    echo "🚀 仮想環境を使用して接続テストを実行..."
    source venv/bin/activate
    python db_connection_test_prod.py
    deactivate
else
    echo "🚀 システムPythonを使用して接続テストを実行..."
    python db_connection_test_prod.py
fi

echo
echo "=================================================="
echo "テスト完了"
echo "=================================================="