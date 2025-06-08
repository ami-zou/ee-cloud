import { useState } from 'react'

export default function JobSubmitForm() {
  const apiBase = "http://cloud.esmeraldacloud.com"
  const jobUrl = `${apiBase}/jobs`

  const [type, setType] = useState<'docker' | 'github'>('docker')
  const [image, setImage] = useState('nginx')
  const [repo, setRepo] = useState('')
  const [cmd, setCmd] = useState('')
  const [env, setEnv] = useState('')
  const [port, setPort] = useState(7860)
  const [response, setResponse] = useState<any>(null)
  const [jobLogs, setJobLogs] = useState<string | null>(null)

  async function submitJob(e: React.FormEvent) {
    e.preventDefault()

    const payload: any = { type }
    if (type === 'docker') payload.image = image
    if (type === 'github') payload.repo = repo
    if (cmd) payload.startup_cmd = cmd
    if (env) {
      try {
        payload.env = JSON.parse(env)
      } catch {
        alert('ENV must be valid JSON')
        return
      }
    }
    payload.expose_port = port

    const res = await fetch(jobUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    const data = await res.json()
    setResponse(data)
    setJobLogs(null)
  }

  async function checkStatus() {
    if (!response?.job_id) return
    const res = await fetch(`${apiBase}/jobs/${response.job_id}`)
    const data = await res.json()
    alert(`Job status: ${data.status}`)
  }

  async function fetchLogs() {
    if (!response?.job_id) return
    const res = await fetch(`${apiBase}/jobs/${response.job_id}/logs`)
    const logs = await res.text()
    setJobLogs(logs)
  }

  async function stopJob() {
    if (!response?.job_id) return
    await fetch(`${apiBase}/jobs/${response.job_id}/stop`, { method: 'POST' })
    alert('Job stopped')
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Job Submission</h2>
      <form onSubmit={submitJob}>
        <label>
          Job Type:
          <select value={type} onChange={(e) => setType(e.target.value as any)}>
            <option value="docker">Docker</option>
            <option value="github">GitHub</option>
          </select>
        </label>
        {type === 'docker' && (
          <label>
            Docker Image:
            <input value={image} onChange={(e) => setImage(e.target.value)} />
          </label>
        )}
        {type === 'github' && (
          <label>
            GitHub Repo URL:
            <input value={repo} onChange={(e) => setRepo(e.target.value)} />
          </label>
        )}
        <label>
          Startup Command (optional):
          <input value={cmd} onChange={(e) => setCmd(e.target.value)} />
        </label>
        <label>
          Exposed Port:
          <input type="number" value={port} onChange={(e) => setPort(parseInt(e.target.value))} />
        </label>
        <label>
          Env Vars (JSON format):
          <textarea value={env} onChange={(e) => setEnv(e.target.value)} />
        </label>
        <button type="submit">Submit Job</button>
      </form>

      {response && (
        <div style={{ marginTop: 20 }}>
          <h3>Job Submitted:</h3>
          <pre>{JSON.stringify(response, null, 2)}</pre>

          <button onClick={checkStatus}>Check Status</button>
          <button onClick={fetchLogs}>View Logs</button>
          <button onClick={stopJob}>Stop Job</button>
        </div>
      )}

      {jobLogs && (
        <div style={{ marginTop: 20 }}>
          <h3>Logs</h3>
          <pre style={{ whiteSpace: 'pre-wrap', background: '#f0f0f0', padding: '1em' }}>{jobLogs}</pre>
        </div>
      )}
    </div>
  )
}