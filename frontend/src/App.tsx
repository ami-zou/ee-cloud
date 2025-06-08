import { useState } from 'react'
import './App.css'

function App() {
  const [prompt, setPrompt] = useState('')
  const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; text: string }[]>([])
  // const apiUrl = import.meta.env.VITE_CHAT_API_URL

  const apiUrl = "http://cloud.esmeraldacloud.com/chat"
  console.log('Chat API URL (env):', apiUrl)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    if (!prompt.trim()) return
    setMessages((prev) => [...prev, { sender: 'user', text: prompt }])

    try {
      const res = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      })
      const data = await res.json()
      setMessages((prev) => [...prev, { sender: 'bot', text: data.response }])
    } catch (err) {
      setMessages((prev) => [...prev, { sender: 'bot', text: 'Error talking to server' }])
    }

    setPrompt('')
  }

  return (
    <div className="chat-container">
      <h1>🪸 Esmeralda Chat</h1>
      <div className="chat-box">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.sender}`}>
            <span>{m.text}</span>
          </div>
        ))}
      </div>
      <form className="input-form" onSubmit={handleSubmit}>
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Ask something..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  )
}

export default App