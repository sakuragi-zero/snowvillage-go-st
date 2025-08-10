"""
初期データ挿入スクリプト
"""
import asyncio
import sys
import os

# プロジェクトルートを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure.database.connection import db
from infrastructure.repositories.mission_repository_impl import MissionRepositoryImpl
from domain.entities.mission import Mission


async def initialize_missions():
    """初期ミッションデータを挿入"""
    mission_repo = MissionRepositoryImpl()
    
    # 既存のミッション確認
    existing_missions = await mission_repo.list_all()
    if existing_missions:
        print(f"既存のミッションが{len(existing_missions)}件見つかりました。スキップします。")
        return
    
    initial_missions = [
        Mission(1, '基本の挨拶', '👋', '基本的な挨拶を学びましょう', 5, 50, 10, 0),
        Mission(2, '自己紹介', '🙋', '自己紹介の方法を学びましょう', 7, 70, 15, 1),
        Mission(3, '家族について', '👨‍👩‍👧‍👦', '家族に関する表現を学びましょう', 6, 60, 12, 2),
        Mission(4, '食べ物と飲み物', '🍽️', '食事に関する表現を学びましょう', 8, 80, 20, 3),
        Mission(5, '時間と日付', '⏰', '時間の表現を学びましょう', 6, 65, 15, 4)
    ]
    
    for mission in initial_missions:
        try:
            created_mission = await mission_repo.create(mission)
            print(f"ミッション作成成功: {created_mission.title}")
        except Exception as e:
            print(f"ミッション作成エラー ({mission.title}): {e}")


async def main():
    """メイン実行関数"""
    print("データベース初期化開始...")
    
    # テーブル作成
    db.create_tables()
    print("テーブル作成完了")
    
    # ミッションデータ挿入
    await initialize_missions()
    print("初期データ挿入完了")


if __name__ == "__main__":
    asyncio.run(main())