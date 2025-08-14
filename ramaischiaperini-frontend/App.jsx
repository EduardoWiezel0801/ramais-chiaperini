import './App.css'
import { useAuth } from './src/hooks/useAuth'
import { useMessage } from './src/hooks/useMessage'
import LoginPage from './src/pages/LoginPage'
import Dashboard from './src/pages/Dashboard'
import LoadingSpinner from './src/components/common/LoadingSpinner'

function App() {
  const { user, loading, login, logout, isAuthenticated } = useAuth()
  const { message, showMessage, clearMessage } = useMessage()

  const handleLogin = async (username, password) => {
    const result = await login(username, password)
    showMessage(result.success ? 'success' : 'error', result.message)
  }

  const handleLogout = async () => {
    const result = await logout()
    showMessage(result.success ? 'success' : 'error', result.message)
  }

  if (loading) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center' 
      }}>
        <LoadingSpinner message="Inicializando aplicação..." />
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <LoginPage 
        onLogin={handleLogin} 
        message={message} 
      />
    )
  }

  return (
    <Dashboard 
      user={user}
      onLogout={handleLogout}
      message={message}
      clearMessage={clearMessage}
      showMessage={showMessage}
    />
  )
}

export default App