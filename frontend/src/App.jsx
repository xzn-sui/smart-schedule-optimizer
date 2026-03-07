import { useState } from 'react'

export default function App() {
  const [response, setResponse] = useState(null)
  const [error, setError] = useState(null)

  async function testBackend() {
    setResponse(null)
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/health')
      const data = await res.json()
      setResponse(JSON.stringify(data))
    } catch (e) {
      setError('Failed to reach backend: ' + e.message)
    }
  }

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '2rem' }}>
      <h1>Smart Schedule Optimizer</h1>
      <button onClick={testBackend}>Test Backend</button>
      {response && <p>Response: {response}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  )
}
