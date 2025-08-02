"""Snow Village UI - ログイン/登録画面モジュール"""

import streamlit as st


def launch_screen():
    """Snow Village のログイン/登録画面を表示"""
    
    # 名前の状態管理
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    
    # 画像をbase64エンコード
    import os
    import base64
    
    # ロゴ画像
    logo_base64 = ""
    logo_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "SnowVillageLogo.png")
    
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
    
    # 背景画像
    bg_base64 = ""
    bg_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "bg-villag-go.png")
    
    if os.path.exists(bg_path):
        with open(bg_path, "rb") as img_file:
            bg_base64 = base64.b64encode(img_file.read()).decode()
    
    # ロゴ部分のHTML
    if logo_base64:
        logo_html = f"""
        <div style="margin-bottom: 1.5rem;">
            <img src="data:image/png;base64,{logo_base64}" 
                 class="logo"
                 style="width: 80px; height: 80px; margin: 0 auto; display: block;" 
                 alt="SnowVillage Logo">
        </div>
        """
    else:
        logo_html = """
        <div style="margin-bottom: 1.5rem;">
            <div style="
                width: 80px;
                height: 80px;
                margin: 0 auto;
                background: #60a5fa;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.5rem;
                color: white;
            ">❄️</div>
        </div>
        """
    
    # JavaScriptで統合されたコンポーネントを作成
    component_html = f"""
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @media (max-width: 768px) {{
            .container {{
                padding: 1rem !important;
                min-height: 100vh !important;
            }}
            .card {{
                padding: 2rem 1.5rem !important;
                margin: 1rem auto !important;
                max-width: 90% !important;
            }}
            .title {{
                font-size: 2.5rem !important;
            }}
            .subtitle {{
                font-size: 1rem !important;
            }}
            .features {{
                font-size: 0.9rem !important;
                margin-bottom: 1.5rem !important;
            }}
            .input, .button {{
                font-size: 1rem !important;
                padding: 0.8rem !important;
            }}
        }}
        @media (max-width: 480px) {{
            .container {{
                padding: 0.5rem !important;
            }}
            .card {{
                padding: 1.5rem 1rem !important;
                margin: 0.5rem auto !important;
                max-width: 95% !important;
                border-radius: 12px !important;
            }}
            .title {{
                font-size: 2rem !important;
                margin-bottom: 0.3rem !important;
            }}
            .subtitle {{
                font-size: 0.9rem !important;
                margin-bottom: 1.5rem !important;
            }}
            .logo {{
                width: 60px !important;
                height: 60px !important;
            }}
        }}
    </style>
    <div class="container" style="
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 80vh;
        padding: 2rem;
    ">
        <div class="card" style="
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.3);
            border-radius: 16px;
            padding: 3rem 2.5rem;
            text-align: center;
            max-width: 450px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        ">
            <!-- ロゴ -->
            {logo_html}
            
            <!-- タイトル -->
            <h1 class="title" style="
                color: white;
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            ">SnowVillage GO</h1>
            
            <!-- サブタイトル -->
            <p class="subtitle" style="
                color: #cbd5e1;
                font-size: 1.2rem;
                margin-bottom: 2rem;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            ">Snowflake World Tour Tokyo 2025</p>
            
            <!-- 機能リスト -->
            <div class="features" style="
                color: #94a3b8;
                font-size: 1rem;
                margin-bottom: 2rem;
            ">
                <div style="margin: 0.5rem 0;">✓ Snowflakeを知る</div>
                <div style="margin: 0.5rem 0;">✓ クエストとチャレンジ</div>
                <div style="margin: 0.5rem 0;">✓ ランキングと景品</div>
            </div>
            
            <!-- 入力フィールド -->
            <input 
                type="text" 
                id="userName"
                class="input"
                placeholder="名前を入力してください"
                style="
                    background: white;
                    border: 2px solid #e2e8f0;
                    border-radius: 12px;
                    padding: 1rem;
                    font-size: 1.1rem;
                    margin-bottom: 1rem;
                    width: 100%;
                    box-sizing: border-box;
                    -webkit-appearance: none;
                    -moz-appearance: none;
                    appearance: none;
                "
                value="{st.session_state.user_name}"
                onchange="window.parent.postMessage({{type: 'nameChange', value: this.value}}, '*')"
            />
            
            <!-- 遊びに行くボタン -->
            <button 
                onclick="submitForm('play')"
                class="button"
                style="
                    background: white;
                    color: #3730a3;
                    border: none;
                    border-radius: 12px;
                    padding: 1rem 2rem;
                    font-size: 1.1rem;
                    font-weight: 600;
                    width: 100%;
                    height: 60px;
                    margin-bottom: 1rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    -webkit-appearance: none;
                    -moz-appearance: none;
                    appearance: none;
                    touch-action: manipulation;
                "
                onmouseover="this.style.background='#f8fafc'; this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 25px rgba(0, 0, 0, 0.15)'"
                onmouseout="this.style.background='white'; this.style.transform='translateY(0)'; this.style.boxShadow='none'"
            >遊びに行く！</button>
            
            <!-- 登録済みボタン -->
            <button 
                onclick="submitForm('login')"
                class="button"
                style="
                    background: transparent;
                    color: white;
                    border: 2px solid rgba(255, 255, 255, 0.3);
                    border-radius: 12px;
                    padding: 1rem 2rem;
                    font-size: 1.1rem;
                    font-weight: 600;
                    width: 100%;
                    height: 60px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    -webkit-appearance: none;
                    -moz-appearance: none;
                    appearance: none;
                    touch-action: manipulation;
                "
                onmouseover="this.style.background='rgba(255, 255, 255, 0.1)'; this.style.borderColor='rgba(255, 255, 255, 0.5)'"
                onmouseout="this.style.background='transparent'; this.style.borderColor='rgba(255, 255, 255, 0.3)'"
            >登録済みの方はこちら</button>
        </div>
    </div>
    
    <script>
        function submitForm(intent) {{
            const userName = document.getElementById('userName').value;
            if (!userName.trim()) {{
                alert('名前を入力してください');
                return;
            }}
            window.parent.postMessage({{
                type: 'submit',
                name: userName.trim(),
                intent: intent
            }}, '*');
        }}
        
        // 名前の変更を監視
        window.addEventListener('message', function(event) {{
            if (event.data.type === 'updateName') {{
                document.getElementById('userName').value = event.data.value;
            }}
        }});
    </script>
    """
    
    # カスタムCSS
    if bg_base64:
        bg_style = f"background: url(data:image/png;base64,{bg_base64}) no-repeat center center fixed; background-size: cover;"
    else:
        bg_style = """background: linear-gradient(
            135deg,
            #1e2a78 0%,
            #3730a3 50%,
            #4338ca 100%
        );"""
    
    st.markdown(f"""
    <style>
    .stApp {{
        {bg_style}
        min-height: 100vh;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # HTMLコンポーネントを表示
    st.components.v1.html(component_html, height=700)
    
    return None


if __name__ == "__main__":
    st.set_page_config(
        page_title="Snow Village - プログラミング学習",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # サイドバーを非表示
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    result = launch_screen()
    
    if result:
        st.balloons()
        st.success(f"🎉 ようこそ {result['name']} さん！")
        
        if result['intent'] == 'play':
            st.info("SnowVillage GOの世界へ！Snowflakeを学びながら楽しみましょう！")
        elif result['intent'] == 'login':
            st.info("おかえりなさい！続きから始めましょう！")
        
        with st.expander("デバッグ情報"):
            st.json(result)