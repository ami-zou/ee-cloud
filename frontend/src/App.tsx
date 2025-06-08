import { useState } from 'react'
import './App.css'
import JobSubmitForm from './JobSubmitForm'

function App() {
  const [activeTab, setActiveTab] = useState<'chat' | 'jobs'>('chat')
  const [prompt, setPrompt] = useState('')
  const [messages, setMessages] = useState<{ sender: 'user' | 'bot'; text: string }[]>([])

  const apiBase = "http://cloud.esmeraldacloud.com"
  const chatUrl = `${apiBase}/chat`
  console.log('Chat API URL (env) is:', apiBase)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setMessages(prev => [...prev, { sender: 'user', text: prompt }])
    try {
      const res = await fetch(chatUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      })
      const data = await res.json()
      setMessages(prev => [...prev, { sender: 'bot', text: data.response }])
    } catch (err) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Error talking to server' }])
    }

    setPrompt('')
  }

  return (
    <div className="app-container">
      <nav>
        <button onClick={() => setActiveTab('chat')}>Chat</button>
        <button onClick={() => setActiveTab('jobs')}>Submit Job</button>
      </nav>

      {activeTab === 'chat' ? (
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
      ) : (
        <JobSubmitForm />
      )}
    </div>
  )
}

export default App