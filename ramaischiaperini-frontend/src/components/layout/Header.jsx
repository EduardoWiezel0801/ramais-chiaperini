import logoChiaperini from '../../assets/logo-chiaperini.png'
import logoTechto from '../../assets/logo-techto.png'

function Header({ user, onLogout }) {
  // Verificações de segurança
  const userName = user?.username || user?.first_name || 'Usuário'
  const avatarLetter = userName.charAt(0).toUpperCase()

  return (
    <header className="header-modern">
      {/* Background animado */}
      <div className="header-bg-animation">
        <div className="bg-shapes">
          <div className="shape shape-1"></div>
          <div className="shape shape-2"></div>
          <div className="shape shape-3"></div>
          <div className="shape shape-4"></div>
          <div className="shape shape-5"></div>
        </div>
        <div className="gradient-overlay"></div>
      </div>

      {/* Partículas flutuantes */}
      <div className="floating-particles">
        <div className="particle"></div>
        <div className="particle"></div>
        <div className="particle"></div>
        <div className="particle"></div>
        <div className="particle"></div>
        <div className="particle"></div>
      </div>

      <div className="header-content-modern">
        <div className="header-logos-modern">
          <div className="logo-container">
            <img 
              src={logoChiaperini} 
              alt="Chiaperini" 
              className="logo-chiaperini-modern"
            />
            <div className="logo-glow"></div>
          </div>
          
          <div className="header-title-container">
            <h1 className="logo-text-modern">
              <span className="title-word">Ramais</span>
            </h1>
          </div>
          
          <div className="logo-container">
            <img 
              src={logoTechto} 
              alt="Techto" 
              className="logo-techto-modern"
            />
            <div className="logo-glow"></div>
          </div>
        </div>

        <div className="user-info-modern">
          <div className="user-avatar">
            <span className="avatar-text">{avatarLetter}</span>
          </div>
          <div className="user-details">
            <span className="user-greeting">Olá,</span>
            <span className="user-name-modern">{userName}</span>
          </div>
          <button className="logout-btn-modern" onClick={onLogout}>
            <span className="btn-text">Sair</span>
            <div className="btn-bg"></div>
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header