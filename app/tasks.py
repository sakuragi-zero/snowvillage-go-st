import yaml
from task_db import TaskService

def load_tasks_from_yaml(yaml_path: str):
    """YAMLファイルからタスクを読み込み"""
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["tasks"]

def sync_yaml_to_db(yaml_path: str):
    """YAMLのタスクをDBに同期（最適化版）"""
    from task_db import _TASKS_SYNCED
    import streamlit as st
    
    # 既に同期済みかチェック
    if _TASKS_SYNCED or (hasattr(st.session_state, '_tasks_synced') and st.session_state._tasks_synced):
        return
    
    task_service = TaskService()
    tasks = load_tasks_from_yaml(yaml_path)
    
    # 一括処理で効率化
    task_service.bulk_insert_tasks_if_not_exists(tasks)
    
    # 同期完了フラグを設定
    globals()['_TASKS_SYNCED'] = True
    st.session_state._tasks_synced = True
    print(f"Task synchronization completed for {len(tasks)} tasks")
