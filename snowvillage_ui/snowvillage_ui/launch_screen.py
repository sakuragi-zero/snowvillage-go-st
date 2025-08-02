# """
# Snow Village - メインアプリケーション
# ログイン画面を表示し、成功後に他のページへ遷移します。
# """

# import streamlit as st
# import os
# import base64
# import time

# def handle_submit(intent: str):
#     """
#     ボタンがクリックされたときに呼び出されるコールバック関数。
#     入力された名前を検証し、結果をセッションに保存します。
#     """
#     name = st.session_state.get("user_name_input", "")
#     if name and name.strip():
#         # 検証成功。結果を'result'キーで保存。
#         st.session_state.result = {
#             "name": name.strip(),
#             "intent": intent
#         }
#         # エラーメッセージが残っていれば削除
#         if 'error_message' in st.session_state:
#             del st.session_state.error_message
#     else:
#         # 検証失敗。エラーメッセージを保存。
#         st.session_state.error_message = "名前を入力してください"

# def launch_screen():
#     """
#     ログイン画面のUIを構築・表示し、ログイン成功時にユーザーデータを返します。
#     """
#     if 'result' in st.session_state and st.session_state.result:
#         result = st.session_state.result
#         del st.session_state.result
#         return result

#     # --- 1. 画像とスタイルの設定 ---
#     def get_base64_img(path):
#         if os.path.exists(path):
#             with open(path, "rb") as img_file:
#                 return base64.b64encode(img_file.read()).decode()
#         return ""

#     base_dir = os.path.dirname(__file__)
#     logo_path = os.path.join(base_dir, "..", "snowvillage_ui", "frontend", "public", "SnowVillageLogo.png")
#     bg_path = os.path.join(base_dir, "..", "snowvillage_ui", "frontend", "public", "bg-villag-go.png")
    
#     logo_base64 = get_base64_img(logo_path)
#     bg_base64 = get_base64_img(bg_path)

#     bg_style = f"background: url(data:image/png;base64,{bg_base64}) no-repeat center center fixed; background-size: cover;" if bg_base64 else "background: linear-gradient(135deg, #1e2a78, #3730a3, #4338ca);"
#     st.markdown(f"""
#     <style>
#         .stApp {{ {bg_style} }}
#         .card {{
#             background: rgba(30, 41, 59, 0.9);
#             border: 1px solid rgba(148, 163, 184, 0.3);
#             border-radius: 16px;
#             padding: 2.5rem;
#             text-align: center;
#             max-width: 450px;
#             margin: 1rem auto;
#             box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
#         }}
#         .stButton button {{
#             border-radius: 12px !important;
#             height: 50px;
#             font-weight: 600;
#         }}
#         .stTextInput input {{
#             border-radius: 12px !important;
#             padding: 1rem !important;
#             height: 50px;
#             border: 2px solid #e2e8f0 !important;
#             background: white !important;
#         }}
#     </style>
#     """, unsafe_allow_html=True)

#     # --- 2. UI要素の配置 ---
#     _left_gap, center_col, _right_gap = st.columns([1, 2, 1])
#     with center_col:
#         # --- 上の黒い部分 (カード) ---
#         st.markdown('<div class="card">', unsafe_allow_html=True)
        
#         if logo_base64:
#             st.image(f"data:image/png;base64,{logo_base64}", width=60)
#         else:
#             st.markdown("<div style='font-size: 40px;'>❄️</div>", unsafe_allow_html=True)

#         # テキストコンテンツを一つのmarkdownにまとめる
#         card_content_html = """
#         <h1 style="color: white; font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem;">SnowVillage GO</h1>
#         <p style="color: #cbd5e1; font-size: 1.1rem; margin-bottom: 1.5rem;">Snowflake World Tour Tokyo 2025</p>
#         <div style="color: #94a3b8; font-size: 1rem; text-align: left; max-width: 200px; margin-left: auto; margin-right: auto; margin-bottom: 1.5rem;">
#             <div style="margin: 0.5rem 0;">✓ Snowflakeを知る</div>
#             <div style="margin: 0.5rem 0;">✓ クエストとチャレンジ</div>
#             <div style="margin: 0.5rem 0;">✓ ランキングと景品</div>
#         </div>
#         """
#         st.markdown(card_content_html, unsafe_allow_html=True)

#         st.text_input(
#             "名前",
#             placeholder="名前を入力してください",
#             key="user_name_input",
#             label_visibility="collapsed"
#         )
        
#         st.markdown('</div>', unsafe_allow_html=True)

#         # --- 下のボタン部分 ---
#         if 'error_message' in st.session_state and st.session_state.error_message:
#             st.error(st.session_state.error_message, icon="⚠️")
#             del st.session_state.error_message

#         btn_col1, btn_col2 = st.columns(2)
#         with btn_col1:
#             st.button("遊びに行く！", use_container_width=True, on_click=handle_submit, args=('play',))
#         with btn_col2:
#             st.button("登録済みの方はこちら", use_container_width=True, on_click=handle_submit, args=('login',))
    
#     return None

# # ==================================================================
# # --- アプリケーションのメイン実行ブロック ---
# # ==================================================================
# st.set_page_config(
#     page_title="ようこそ Snow Villageへ",
#     page_icon="❄️",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# st.markdown("<style>[data-testid='stSidebar'] { display: none; }</style>", unsafe_allow_html=True)

# if "user_info" not in st.session_state:
#     st.session_state.user_info = None

# login_result = launch_screen()

# if login_result:
#     st.session_state.user_info = login_result
#     st.balloons()
#     st.success(f"🎉 ようこそ {st.session_state.user_info['name']} さん！")
#     st.info("チャレンジページへ移動します...")
#     time.sleep(2)
#     st.switch_page("pages/challenge_page.py")