import React, { useState } from "react"
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib"

function MyComponent() {
  const [name, setName] = useState("")
  const [mode, setMode] = useState<"login" | "register" | null>(null)

  const handleSubmit = () => {
    if (!name || !mode) return
    Streamlit.setComponentValue({ name, intent: mode })
  }

  return (
    <div style={{ textAlign: "center", padding: "2rem", background: "#f0f0f0" }}>
      <h1>Snow Village へようこそ！</h1>
      <input
        type="text"
        placeholder="名前を入力"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{ padding: "0.5rem", margin: "1rem" }}
      />
      <div>
        <button onClick={() => { setMode("register"); handleSubmit() }}>
          登録
        </button>
        <button onClick={() => { setMode("login"); handleSubmit() }} style={{ marginLeft: "1rem" }}>
          ログイン
        </button>
      </div>
    </div>
  )
}

export default withStreamlitConnection(MyComponent)