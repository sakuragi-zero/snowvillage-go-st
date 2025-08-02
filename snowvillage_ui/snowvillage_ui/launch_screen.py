import streamlit as st
import streamlit.components.v1 as components
import os

def launch_screen():
    """Snow Village のログイン/登録画面を表示"""
    
    st.markdown("""
    <div style="
        text-align: center; 
        padding: 2rem; 
        background: #f0f0f0; 
        border-radius: 10px;
        margin: 20px 0;
    ">
        <h1 style="color: #333;">Snow Village へようこそ！</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        name = st.text_input("名前を入力してください", key="user_name")
        
        col_reg, col_login = st.columns(2)
        
        with col_reg:
            if st.button("🔒 登録", use_container_width=True):
                if name:
                    return {"name": name, "intent": "register"}
                else:
                    st.error("名前を入力してください")
        
        with col_login:
            if st.button("🚪 ログイン", use_container_width=True):
                if name:
                    return {"name": name, "intent": "login"}
                else:
                    st.error("名前を入力してください")
    
    return None

# メインアプリ
if __name__ == "__main__":
    st.set_page_config(
        page_title="Snow Village", 
        page_icon="❄️",
        layout="wide"
    )
    
    result = launch_screen()
    
    if result:
        st.success(f"ユーザー: {result['name']} - アクション: {result['intent']}")
        st.json(result)