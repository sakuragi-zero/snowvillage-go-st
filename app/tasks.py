import yaml
from task_db import TaskService

def load_tasks_from_yaml(yaml_path: str):
    """YAMLファイルからタスクを読み込み"""
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["tasks"]

def sync_yaml_to_db(yaml_path: str):
    """YAMLのタスクをDBに同期"""
    task_service = TaskService()
    tasks = load_tasks_from_yaml(yaml_path)
    for task in tasks:
        task_service.insert_task_if_not_exists(task["id"], task["title"])
