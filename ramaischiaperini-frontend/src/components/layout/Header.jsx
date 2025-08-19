function Header({ user, onLogout }) {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="logo">Ramais</h1>
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