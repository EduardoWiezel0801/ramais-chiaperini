import { useState } from 'react'
import Alert from '../components/common/Alert'

function LoginPage({ onLogin, message }) {
  const [credentials, setCredentials] = useState({ username: '', password: '' })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    await onLogin(credentials.username, credentials.password)
    setLoading(false)
  }

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h1 className="login-title">Sistema de Ramais</h1>
        
        <Alert type={message.type} message={message.text} />

        <div className="form-group">
          <label className="form-label">Usuário</label>
          <input
            type="text"
            className="form-input"
            value={credentials.username}
            onChange={(e) => setCredentials({...credentials, username: e.target.value})}
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Senha</label>
          <input
            type="password"
            className="form-input"
            value={credentials.password}
            onChange={(e) => setCredentials({...credentials, password: e.target.value})}
            required
            disabled={loading}
          />
        </div>

        <button 
          type="submit" 
          className="btn btn-primary" 
          style={{width: '100%'}}
          disabled={loading}
        >
          {loading ? 'Entrando...' : 'Entrar'}
        </button>

        <div style={{marginTop: '1rem', fontSize: '0.875rem', color: '#64748b', textAlign: 'center'}}>
          <p><strong>Admin:</strong> admin / admin123</p>
          <p><strong>Usuário:</strong> usuario / user123</p>
        </div>
      </form>
    </div>
  )
}

export default LoginPage