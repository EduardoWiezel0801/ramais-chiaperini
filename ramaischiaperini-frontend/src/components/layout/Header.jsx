function Header({ user, onLogout }) {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="logo">Sistema de Ramais - Chiaperini</h1>
        <div className="user-info">
          <span className="user-name">Olá, {user.username}</span>
          <button className="logout-btn" onClick={onLogout}>
            Sair
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header