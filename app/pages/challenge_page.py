"""チャレンジページ"""

import streamlit as st
import json
from datetime import datetime
from app.database.models import Challenge, UserProgress
from app.database.db_manager import DatabaseManager
from app.auth.session_manager import SessionManager


class ChallengePage:
    """チャレンジページクラス"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.session_manager = SessionManager(db)
    
    def render(self):
        """チャレンジページをレンダリング"""
        # ログイン確認
        if not self.session_manager.is_logged_in():
            st.error("ログインが必要です。")
            st.stop()
        
        current_user = self.session_manager.get_current_user()
        if not current_user:
            st.error("ユーザー情報を取得できませんでした。")
            st.stop()
        
        # チャレンジID確認
        challenge_id = st.session_state.get('current_challenge_id')
        if not challenge_id:
            st.error("チャレンジが選択されていません。")
            self._render_back_button()
            st.stop()
        
        # チャレンジ取得
        challenge = self._get_challenge(challenge_id)
        if not challenge:
            st.error("チャレンジが見つかりませんでした。")
            self._render_back_button()
            st.stop()
        
        # スタイル適用
        self._render_styles()
        
        # チャレンジ表示
        self._render_challenge(challenge, current_user)
    
    def _render_styles(self):
        """ページスタイルを適用"""
        st.markdown("""
        <style>
        .challenge-header {
            background: linear-gradient(135deg, #1e2a78, #3730a3, #4338ca);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .question-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .option-button {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            width: 100%;
            text-align: left;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .option-button:hover {
            border-color: #3730a3;
            box-shadow: 0 4px 15px rgba(55, 48, 163, 0.2);
        }
        
        .option-button.selected {
            border-color: #3730a3;
            background: #f8fafc;
        }
        
        .option-button.correct {
            border-color: #10b981;
            background: #f0fdf4;
            color: #065f46;
        }
        
        .option-button.incorrect {
            border-color: #ef4444;
            background: #fef2f2;
            color: #991b1b;
        }
        
        .result-card {
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin: 2rem 0;
        }
        
        .result-success {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
        }
        
        .result-failure {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
        }
        
        .difficulty-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            color: white;
            margin-left: 0.5rem;
        }
        
        .difficulty-1 { background: #10b981; }
        .difficulty-2 { background: #f59e0b; }
        .difficulty-3 { background: #ef4444; }
        </style>
        """, unsafe_allow_html=True)
    
    def _render_challenge(self, challenge: Challenge, current_user):
        """チャレンジを表示"""
        # ヘッダー
        st.markdown(f"""
        <div class="challenge-header">
            <h1>🎯 {challenge.title}</h1>
            <span class="difficulty-badge difficulty-{challenge.difficulty}">
                レベル {challenge.difficulty}
            </span>
            <p>{challenge.description}</p>
            <p><strong>獲得ポイント:</strong> {challenge.points} pt</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 戻るボタン
        self._render_back_button()
        
        # 問題表示
        self._render_question(challenge, current_user)
    
    def _render_question(self, challenge: Challenge, current_user):
        """問題を表示"""
        st.markdown(f"""
        <div class="question-card">
            <h2>📝 問題</h2>
            <p style="font-size: 1.2rem; line-height: 1.6;">{challenge.question}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 回答状態の管理
        answer_key = f"answer_{challenge.id}"
        result_key = f"result_{challenge.id}"
        
        # 選択肢表示
        if challenge.options:
            st.markdown("### 選択肢を選んでください:")
            
            selected_option = st.radio(
                "",
                options=challenge.options,
                key=answer_key,
                label_visibility="collapsed"
            )
            
            # 回答ボタン
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🎯 回答する", use_container_width=True, key=f"submit_{challenge.id}"):
                    result = self._check_answer(challenge, selected_option, current_user)
                    st.session_state[result_key] = result
                    st.rerun()
        else:
            # テキスト入力形式
            user_answer = st.text_input(
                "回答を入力してください:",
                key=answer_key
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🎯 回答する", use_container_width=True, key=f"submit_{challenge.id}"):
                    if user_answer.strip():
                        result = self._check_answer(challenge, user_answer.strip(), current_user)
                        st.session_state[result_key] = result
                        st.rerun()
                    else:
                        st.error("回答を入力してください。")
        
        # 結果表示
        if result_key in st.session_state:
            result = st.session_state[result_key]
            self._render_result(result, challenge)
    
    def _render_result(self, result: dict, challenge: Challenge):
        """結果を表示"""
        if result['correct']:
            st.markdown(f"""
            <div class="result-card result-success">
                <h2>🎉 正解！</h2>
                <p>素晴らしい！{challenge.points}ポイント獲得しました。</p>
                <p><strong>正解:</strong> {challenge.correct_answer}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 次のチャレンジボタン
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🚀 次のチャレンジへ", use_container_width=True):
                    # セッション状態をクリア
                    for key in list(st.session_state.keys()):
                        if key.startswith(f"answer_{challenge.id}") or key.startswith(f"result_{challenge.id}"):
                            del st.session_state[key]
                    
                    st.session_state.page = "learning"
                    if 'current_challenge_id' in st.session_state:
                        del st.session_state['current_challenge_id']
                    st.rerun()
        else:
            st.markdown(f"""
            <div class="result-card result-failure">
                <h2>❌ 不正解</h2>
                <p>残念！もう一度挑戦してみましょう。</p>
                <p><strong>正解:</strong> {challenge.correct_answer}</p>
                <p><strong>あなたの回答:</strong> {result['user_answer']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 再挑戦ボタン
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🔄 再挑戦", use_container_width=True):
                    # 結果をクリアして再挑戦
                    result_key = f"result_{challenge.id}"
                    if result_key in st.session_state:
                        del st.session_state[result_key]
                    st.rerun()
    
    def _check_answer(self, challenge: Challenge, user_answer: str, current_user) -> dict:
        """回答をチェック"""
        is_correct = user_answer.strip().lower() == challenge.correct_answer.strip().lower()
        
        # 進捗を記録
        self._record_progress(current_user.id, challenge.id, is_correct, challenge.points if is_correct else 0)
        
        return {
            'correct': is_correct,
            'user_answer': user_answer,
            'points_earned': challenge.points if is_correct else 0
        }
    
    def _record_progress(self, user_id: int, challenge_id: int, completed: bool, score: int):
        """進捗を記録"""
        try:
            with self.db.get_connection() as conn:
                # 既存の進捗を確認
                existing = conn.execute("""
                    SELECT * FROM user_progress 
                    WHERE user_id = ? AND challenge_id = ?
                """, (user_id, challenge_id)).fetchone()
                
                if existing:
                    # 更新
                    conn.execute("""
                        UPDATE user_progress 
                        SET completed = ?, score = ?, attempts = attempts + 1, 
                            completed_at = ?
                        WHERE user_id = ? AND challenge_id = ?
                    """, (
                        completed, 
                        max(existing['score'], score),  # 最高スコアを保持
                        datetime.now().isoformat() if completed else existing['completed_at'],
                        user_id, 
                        challenge_id
                    ))
                else:
                    # 新規作成
                    conn.execute("""
                        INSERT INTO user_progress 
                        (user_id, challenge_id, completed, score, attempts, completed_at)
                        VALUES (?, ?, ?, ?, 1, ?)
                    """, (
                        user_id, 
                        challenge_id, 
                        completed, 
                        score,
                        datetime.now().isoformat() if completed else None
                    ))
                
                conn.commit()
                
        except Exception as e:
            st.error(f"進捗記録エラー: {e}")
    
    def _get_challenge(self, challenge_id: int) -> Challenge:
        """チャレンジを取得"""
        try:
            with self.db.get_connection() as conn:
                row = conn.execute("""
                    SELECT * FROM challenges WHERE id = ?
                """, (challenge_id,)).fetchone()
                
                if row:
                    return Challenge.from_db_row(row)
                return None
                
        except Exception as e:
            st.error(f"チャレンジ取得エラー: {e}")
            return None
    
    def _render_back_button(self):
        """戻るボタンを表示"""
        if st.button("← 学習ページに戻る"):
            # セッション状態をクリア
            if 'current_challenge_id' in st.session_state:
                del st.session_state['current_challenge_id']
            
            st.session_state.page = "learning"
            st.rerun()