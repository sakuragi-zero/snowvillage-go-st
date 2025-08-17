# UI リファクタリング・ナレッジ

## 概要
このドキュメントは、Snow Village ダッシュボードのUIエンハンス時に発見した問題と解決方法を記録しています。

## 実装前の問題点

### 1. 視認性の問題
- **文字色の問題**: 白いテキストが白い背景と重なり読めない
- **コントラスト不足**: グレーテキストが背景に埋もれる
- **枠線なし**: カードの境界が不明確

### 2. デザインの問題
- **絵文字の多用**: プロフェッショナルさに欠ける
- **ボタンの平面感**: 立体感やフィードバックがない
- **統一感の欠如**: 要素ごとにデザインが異なる

### 3. 機能の問題
- **多重入れ子構造**: Streamlitボタンがネストして動作不良
- **レスポンシブ未対応**: モバイル表示が破綻

## 解決アプローチ

### 1. Material Design 導入

```html
<!-- Material Icons CDN -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

**メリット:**
- プロフェッショナルなアイコン
- 統一されたデザイン言語
- アクセシビリティ対応

### 2. カラーシステムの統一

```css
/* プライマリカラー */
--primary-50: #eff6ff;
--primary-500: #3b82f6;
--primary-600: #2563eb;
--primary-700: #1d4ed8;

/* グレースケール */
--gray-50: #f9fafb;
--gray-100: #f3f4f6;
--gray-500: #6b7280;
--gray-900: #111827;
```

**改善点:**
- 十分なコントラスト比（WCAG準拠）
- 一貫したカラーパレット
- 読みやすさの向上

### 3. ボタンの多重入れ子問題の解決

#### 問題の原因
```python
# 問題のあるコード例 - HTMLカード内でボタンを配置
card_html = f"""
<div class="mission-card">
    <button onclick="someFunction()">ボタン</button> # ←動作しない
</div>
"""
st.markdown(card_html, unsafe_allow_html=True)

# または、コンテナ内のボタン
with st.container():
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    if st.button("ボタン"): # ←レイアウトが崩れる、反応しない
        pass
    st.markdown('</div>', unsafe_allow_html=True)
```

#### 解決方法: カード外ボタン配置

```python
# HTMLカード（ボタンなし）
card_html = f"""
<div class="mission-card">
    <div class="mission-info">
        <h3>{task['title']}</h3>
        <p>{task['description']}</p>
    </div>
</div>
"""
st.markdown(card_html, unsafe_allow_html=True)

# カード外にStreamlitボタンを配置
if not is_completed:
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("挑戦", key=f"task_{task_id}", type="primary"):
            st.session_state[f"show_{task_id}"] = True
            st.rerun()
```

#### ❌ 避けるべきパターン
1. **HTMLカード内にボタン**: 動作しない
2. **複雑なJavaScript連携**: 保守困難
3. **非表示ボタンのトリガー**: 複雑で不安定
4. **深いコンテナ入れ子**: レイアウト破綻

### 4. レスポンシブデザイン

```css
@media (max-width: 768px) {
    .main-container {
        margin: 1rem;
        padding: 1.5rem;
        border-radius: 16px;
    }
    
    .card-content {
        flex-direction: column;
        gap: 1rem;
    }
    
    .md-button {
        width: 100%;
    }
}
```

## ベストプラクティス

### 1. CSS設計原則
- **BEM記法**: `.mission-card__title`
- **カスケード活用**: 親クラスで子要素を制御
- **CSS変数**: 一貫したスタイル管理

### 2. Streamlit特有の対処
- **非表示ボタン**: `.stButton { display: none; }`
- **セッション管理**: 状態をst.session_stateで管理
- **リロード制御**: 必要時のみst.rerun()

### 3. アクセシビリティ
- **コントラスト比**: 4.5:1以上を確保
- **キーボード操作**: tabindexとfocus管理
- **セマンティック**: 適切なHTML要素使用

## 実装パターン

### カードコンポーネント
```python
def create_mission_card(task, is_completed):
    return f"""
    <div class="mission-card {'completed' if is_completed else ''}">
        <div class="card-content">
            <div class="mission-info">
                <div class="mission-title">
                    <span class="material-icons mission-type-icon">
                        {get_task_icon(task['type'])}
                    </span>
                    {task['title']}
                </div>
                <div class="mission-description">
                    {task['description']}
                </div>
                <div class="mission-status">
                    <span class="material-icons status-icon">
                        {'check_circle' if is_completed else 'radio_button_unchecked'}
                    </span>
                    {'完了' if is_completed else '未完了'}
                </div>
            </div>
            <div class="mission-actions">
                {create_action_button(task, is_completed)}
            </div>
        </div>
    </div>
    """
```

### 状態管理パターン
```python
def handle_task_interaction(task_id, action_type):
    state_key = f"{action_type}_{task_id}"
    
    # トリガー検出
    if st.session_state.get(f"trigger_{state_key}", False):
        st.session_state[f"show_{state_key}"] = True
        st.session_state[f"trigger_{state_key}"] = False
        st.rerun()
    
    # コンテンツ表示
    if st.session_state.get(f"show_{state_key}", False):
        display_task_content(task_id, action_type)
```

## 注意点とトラブルシューティング

### 1. 最も重要: ボタンをHTMLカード内に配置しない
- **問題**: HTMLカード内のボタンは反応しない
- **解決**: 必ずStreamlitボタンをカード外に配置
- **ベストプラクティス**: `st.columns()`でレイアウト調整

### 2. 空の`<div>`コンテナ削除
- **問題**: `<div class="main-container"></div>`が不要に生成される
- **解決**: 適切なHTML構造設計、不要なコンテナ削除

### 3. Material Icons の制限
- **問題**: 一部アイコン（`quiz`等）で読み取りエラー
- **解決**: 代替アイコンを使用（`quiz` → `school`）

### 4. CSS適用順序
- **問題**: Streamlitデフォルトスタイルの上書き
- **解決**: `!important`や詳細度を調整

### 5. セッション状態の競合
- **問題**: 複数ボタンの同時クリック
- **解決**: ユニークキーとフラグ管理

### 6. 重複ボタンキーエラー
- **問題**: `StreamlitDuplicateElementKey` エラー - 同じキーのボタンが複数存在
- **原因**: 複数の表示関数で同じキー形式を使用（例：`close_sns_{task_id}`）
- **解決**: 
  - ボタンキーに機能別の接尾辞を追加（例：`close_sns_content_{task_id}`）
  - 重複する古い関数を削除
  - セッション状態キーの統一（`show_quiz_{task_id}`, `show_sns_{task_id}`）

## パフォーマンス考慮

### 1. CSS最適化
- **Critical CSS**: 初期表示に必要なスタイルをインライン化
- **レイジーロード**: 非表示コンテンツのCSS遅延読み込み

### 2. JavaScript最適化
- **イベント委譲**: 親要素でイベント管理
- **デバウンス**: 連続クリック防止

### 3. Streamlit最適化
- **@st.cache_resource**: 重い処理をキャッシュ
- **条件分岐**: 不要なコンポーネント生成を避ける

## 今後の改善提案

1. **コンポーネント化**: 再利用可能なUIコンポーネントライブラリ
2. **テーマシステム**: ダーク/ライトモード対応
3. **アニメーション**: マイクロインタラクション追加
4. **PWA対応**: オフライン機能とアプリ化

---

このナレッジを参考に、今後のUI開発で同様の問題を回避し、より良いユーザー体験を提供してください。