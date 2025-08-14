import Header from './Header'
import Alert from '../common/Alert'

function Layout({ user, onLogout, message, clearMessage, children }) {
  return (
    <div className="app">
      <Header user={user} onLogout={onLogout} />
      
      <main className="main-content">
        <Alert 
          type={message.type} 
          message={message.text} 
          onClose={clearMessage}
        />
        {children}
      </main>
    </div>
  )
}

export default Layout