#!/usr/bin/env python3
"""
パフォーマンステストスクリプト
DB初期化とタスク同期の最適化を検証
"""

import time
import sys
import os
from contextlib import contextmanager

# パスを追加してモジュールをインポート
sys.path.append(os.path.dirname(__file__))

@contextmanager
def timer(description):
    """実行時間を測定するコンテキストマネージャー"""
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"{description}: {end - start:.3f}秒")

def reset_global_flags():
    """グローバルフラグをリセット"""
    try:
        from task_db import _DB_INITIALIZED, _TASKS_SYNCED
        import task_db
        task_db._DB_INITIALIZED = False
        task_db._TASKS_SYNCED = False
        print("グローバルフラグをリセットしました")
    except ImportError:
        print("警告: グローバルフラグのリセットに失敗しました")

def test_original_vs_optimized():
    """最適化前後のパフォーマンス比較テスト"""
    print("=== TaskService パフォーマンステスト ===")
    
    # テスト1: 初期化パフォーマンス
    print("\n1. データベース初期化テスト")
    
    reset_global_flags()
    
    # 1回目の初期化（実際にCREATE文が実行される）
    with timer("初回TaskService初期化"):
        from task_db import TaskService
        service1 = TaskService()
    
    # 2回目の初期化（フラグによりスキップされる）
    with timer("2回目TaskService初期化（最適化済み）"):
        service2 = TaskService()
    
    # 3回目の初期化（さらに高速化される）
    with timer("3回目TaskService初期化（最適化済み）"):
        service3 = TaskService()
    
    # テスト2: タスク同期パフォーマンス
    print("\n2. タスク同期テスト")
    
    yaml_path = "tasks.yml"
    if os.path.exists(yaml_path):
        # 1回目の同期（実際にDBアクセスが発生）
        with timer("初回タスク同期"):
            from tasks import sync_yaml_to_db
            sync_yaml_to_db(yaml_path)
        
        # 2回目の同期（フラグによりスキップされる）
        with timer("2回目タスク同期（最適化済み）"):
            sync_yaml_to_db(yaml_path)
            
        # 3回目の同期（さらに高速化される）
        with timer("3回目タスク同期（最適化済み）"):
            sync_yaml_to_db(yaml_path)
    else:
        print("警告: tasks.ymlが見つかりません")
    
    # テスト3: 複数インスタンス作成テスト
    print("\n3. 複数TaskServiceインスタンス作成テスト")
    
    start_time = time.time()
    services = []
    for i in range(5):
        with timer(f"TaskService #{i+1}"):
            service = TaskService()
            services.append(service)
    
    total_time = time.time() - start_time
    print(f"合計時間: {total_time:.3f}秒")
    print(f"平均時間: {total_time/5:.3f}秒")

def test_bulk_vs_individual():
    """一括挿入 vs 個別挿入のパフォーマンス比較"""
    print("\n=== 一括挿入 vs 個別挿入パフォーマンステスト ===")
    
    from task_db import TaskService
    from tasks import load_tasks_from_yaml
    
    yaml_path = "tasks.yml"
    if not os.path.exists(yaml_path):
        print("警告: tasks.ymlが見つからないため、テストをスキップします")
        return
    
    tasks_data = load_tasks_from_yaml(yaml_path)
    service = TaskService()
    
    print(f"テストデータ: {len(tasks_data)}個のタスク")
    
    # テスト用の新しいタスクIDを作成（重複を避けるため）
    test_tasks = []
    base_id = 10000
    for i, task in enumerate(tasks_data[:10]):  # 最初の10個のタスクでテスト
        test_task = task.copy()
        test_task['id'] = base_id + i
        test_task['title'] = f"テストタスク_{i+1}"
        test_tasks.append(test_task)
    
    # まずテストタスクを削除（存在する場合）
    try:
        import psycopg2
        with psycopg2.connect(**service.connection_params) as conn:
            with conn.cursor() as cur:
                for task in test_tasks:
                    cur.execute("DELETE FROM tasks WHERE id = %s", (task['id'],))
            conn.commit()
        print("既存のテストタスクを削除しました")
    except Exception as e:
        print(f"テストタスク削除時エラー: {e}")
    
    # 個別挿入テスト
    with timer("個別挿入（10タスク）"):
        for task in test_tasks:
            service.insert_task_if_not_exists(
                task['id'], 
                task['title'], 
                task.get('type', 'basic'),
                task.get('description'),
                task.get('content')
            )
    
    # テストタスクを再度削除
    try:
        with psycopg2.connect(**service.connection_params) as conn:
            with conn.cursor() as cur:
                for task in test_tasks:
                    cur.execute("DELETE FROM tasks WHERE id = %s", (task['id'],))
            conn.commit()
    except Exception as e:
        print(f"テストタスク削除時エラー: {e}")
    
    # 一括挿入テスト
    with timer("一括挿入（10タスク）"):
        service.bulk_insert_tasks_if_not_exists(test_tasks)
    
    print("テスト完了")

if __name__ == "__main__":
    test_original_vs_optimized()
    test_bulk_vs_individual()
    print("\n=== パフォーマンステスト完了 ===")