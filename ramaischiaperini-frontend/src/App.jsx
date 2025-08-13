import { useState, useEffect } from 'react'
import './App.css'

const API_BASE = 'http://localhost:5000/api'

function App() {
  // Estados principais
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('funcionarios')
  
  // Estados para dados
  const [funcionarios, setFuncionarios] = useState([])
  const [departamentos, setDepartamentos] = useState([])
  const [funcoes, setFuncoes] = useState([])
  const [unidades, setUnidades] = useState([])
  
  // Estados para filtros e busca
  const [busca, setBusca] = useState('')
  const [filtros, setFiltros] = useState({
    departamento_id: '',
    funcao_id: '',
    unidade_id: ''
  })
  
  // Estados para modais
  const [showModal, setShowModal] = useState(false)
  const [modalType, setModalType] = useState('') // 'funcionario', 'departamento', 'funcao', 'unidade'
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({})
  
  // Estados para mensagens
  const [message, setMessage] = useState({ type: '', text: '' })

  // Verificar autenticação ao carregar
  useEffect(() => {
    checkAuth()
  }, [])

  // Carregar dados quando usuário logado
  useEffect(() => {
    if (user) {
      loadAllData()
    }
  }, [user])

  const checkAuth = async () => {
    try {
      const response = await fetch(`${API_BASE}/me`, {
        credentials: 'include'
      })
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      }
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadAllData = async () => {
    try {
      const [funcRes, deptRes, funcaoRes, unidRes] = await Promise.all([
        fetch(`${API_BASE}/funcionarios?busca=${busca}&departamento_id=${filtros.departamento_id}&funcao_id=${filtros.funcao_id}&unidade_id=${filtros.unidade_id}`, { credentials: 'include' }),
        fetch(`${API_BASE}/departamentos`, { credentials: 'include' }),
        fetch(`${API_BASE}/funcoes`, { credentials: 'include' }),
        fetch(`${API_BASE}/unidades`, { credentials: 'include' })
      ])

      if (funcRes.ok) setFuncionarios(await funcRes.json())
      if (deptRes.ok) setDepartamentos(await deptRes.json())
      if (funcaoRes.ok) setFuncoes(await funcaoRes.json())
      if (unidRes.ok) setUnidades(await unidRes.json())
    } catch (error) {
      showMessage('error', 'Erro ao carregar dados')
    }
  }

  const login = async (username, password) => {
    try {
      const response = await fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username, password })
      })

      if (response.ok) {
        const data = await response.json()
        setUser(data.user)
        showMessage('success', 'Login realizado com sucesso!')
      } else {
        const error = await response.json()
        showMessage('error', error.error || 'Erro no login')
      }
    } catch (error) {
      showMessage('error', 'Erro de conexão')
    }
  }

  const logout = async () => {
    try {
      await fetch(`${API_BASE}/logout`, {
        method: 'POST',
        credentials: 'include'
      })
      setUser(null)
      setFuncionarios([])
      setDepartamentos([])
      setFuncoes([])
      setUnidades([])
    } catch (error) {
      console.error('Erro no logout:', error)
    }
  }

  const showMessage = (type, text) => {
    setMessage({ type, text })
    setTimeout(() => setMessage({ type: '', text: '' }), 5000)
  }

  const openModal = (type, item = null) => {
    setModalType(type)
    setEditingItem(item)
    
    if (type === 'funcionario') {
      setFormData(item || {
        nome: '',
        ramal: '',
        email: '',
        whatsapp: '',
        departamento_id: '',
        funcao_id: '',
        unidade_id: ''
      })
    } else {
      setFormData(item || { nome: '' })
    }
    
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setModalType('')
    setEditingItem(null)
    setFormData({})
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    const endpoints = {
      funcionario: 'funcionarios',
      departamento: 'departamentos',
      funcao: 'funcoes',
      unidade: 'unidades'
    }
    
    const endpoint = endpoints[modalType]
    const method = editingItem ? 'PUT' : 'POST'
    const url = editingItem 
      ? `${API_BASE}/${endpoint}/${editingItem.id}`
      : `${API_BASE}/${endpoint}`

    try {
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        showMessage('success', `${modalType} ${editingItem ? 'atualizado' : 'criado'} com sucesso!`)
        closeModal()
        loadAllData()
      } else {
        const error = await response.json()
        showMessage('error', error.error || 'Erro ao salvar')
      }
    } catch (error) {
      showMessage('error', 'Erro de conexão')
    }
  }

  const handleDelete = async (type, id) => {
    if (!confirm('Tem certeza que deseja excluir?')) return

    const endpoints = {
      funcionario: 'funcionarios',
      departamento: 'departamentos',
      funcao: 'funcoes',
      unidade: 'unidades'
    }

    try {
      const response = await fetch(`${API_BASE}/${endpoints[type]}/${id}`, {
        method: 'DELETE',
        credentials: 'include'
      })

      if (response.ok) {
        showMessage('success', `${type} excluído com sucesso!`)
        loadAllData()
      } else {
        const error = await response.json()
        showMessage('error', error.error || 'Erro ao excluir')
      }
    } catch (error) {
      showMessage('error', 'Erro de conexão')
    }
  }

  const clearFilters = () => {
    setBusca('')
    setFiltros({
      departamento_id: '',
      funcao_id: '',
      unidade_id: ''
    })
  }

  // Aplicar filtros quando mudarem
  useEffect(() => {
    if (user) {
      loadAllData()
    }
  }, [busca, filtros])

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        Carregando...
      </div>
    )
  }

  if (!user) {
    return <LoginForm onLogin={login} message={message} />
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <a href="#" className="logo">Sistema de Ramais - Chiaperini</a>
          <div className="user-info">
            <span className="user-name">
              {user.username} {user.is_admin && '(Admin)'}
            </span>
            <button className="logout-btn" onClick={logout}>
              Sair
            </button>
          </div>
        </div>
      </header>

      <main className="main-content">
        {message.text && (
          <div className={`alert alert-${message.type}`}>
            {message.text}
          </div>
        )}

        {user.is_admin && (
          <nav className="nav-tabs">
            <button 
              className={`nav-tab ${activeTab === 'funcionarios' ? 'active' : ''}`}
              onClick={() => setActiveTab('funcionarios')}
            >
              Funcionários
            </button>
            <button 
              className={`nav-tab ${activeTab === 'configuracoes' ? 'active' : ''}`}
              onClick={() => setActiveTab('configuracoes')}
            >
              Configurações
            </button>
          </nav>
        )}

        {activeTab === 'funcionarios' && (
          <FuncionariosTab
            funcionarios={funcionarios}
            departamentos={departamentos}
            funcoes={funcoes}
            unidades={unidades}
            busca={busca}
            setBusca={setBusca}
            filtros={filtros}
            setFiltros={setFiltros}
            clearFilters={clearFilters}
            onEdit={user.is_admin ? (item) => openModal('funcionario', item) : null}
            onDelete={user.is_admin ? (id) => handleDelete('funcionario', id) : null}
            onAdd={user.is_admin ? () => openModal('funcionario') : null}
          />
        )}

        {activeTab === 'configuracoes' && user.is_admin && (
          <ConfiguracoesTab
            departamentos={departamentos}
            funcoes={funcoes}
            unidades={unidades}
            onEdit={(type, item) => openModal(type, item)}
            onDelete={handleDelete}
            onAdd={(type) => openModal(type)}
          />
        )}
      </main>

      {showModal && (
        <Modal
          title={`${editingItem ? 'Editar' : 'Adicionar'} ${modalType}`}
          onClose={closeModal}
        >
          <form onSubmit={handleSubmit}>
            <div className="modal-body">
              {modalType === 'funcionario' ? (
                <FuncionarioForm
                  formData={formData}
                  setFormData={setFormData}
                  departamentos={departamentos}
                  funcoes={funcoes}
                  unidades={unidades}
                />
              ) : (
                <div className="form-group">
                  <label className="form-label">Nome</label>
                  <input
                    type="text"
                    className="form-input"
                    value={formData.nome || ''}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
                    required
                  />
                </div>
              )}
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-outline" onClick={closeModal}>
                Cancelar
              </button>
              <button type="submit" className="btn btn-primary">
                {editingItem ? 'Atualizar' : 'Criar'}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </div>
  )
}

// Componente de Login
function LoginForm({ onLogin, message }) {
  const [credentials, setCredentials] = useState({ username: '', password: '' })

  const handleSubmit = (e) => {
    e.preventDefault()
    onLogin(credentials.username, credentials.password)
  }

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h1 className="login-title">Sistema de Ramais</h1>
        
        {message.text && (
          <div className={`alert alert-${message.type}`}>
            {message.text}
          </div>
        )}

        <div className="form-group">
          <label className="form-label">Usuário</label>
          <input
            type="text"
            className="form-input"
            value={credentials.username}
            onChange={(e) => setCredentials({...credentials, username: e.target.value})}
            required
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
          />
        </div>

        <button type="submit" className="btn btn-primary" style={{width: '100%'}}>
          Entrar
        </button>

        <div style={{marginTop: '1rem', fontSize: '0.875rem', color: '#64748b', textAlign: 'center'}}>
          <p><strong>Admin:</strong> admin / admin123</p>
          <p><strong>Usuário:</strong> usuario / user123</p>
        </div>
      </form>
    </div>
  )
}

// Componente da aba Funcionários
function FuncionariosTab({ 
  funcionarios, departamentos, funcoes, unidades, 
  busca, setBusca, filtros, setFiltros, clearFilters,
  onEdit, onDelete, onAdd 
}) {
  return (
    <>
      <div className="search-filters">
        <div className="search-row">
          <div className="search-input">
            <label className="form-label">Buscar</label>
            <input
              type="text"
              className="form-input"
              placeholder="Nome, ramal ou email..."
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>
          
          <div className="filter-group">
            <div className="filter-item">
              <label className="form-label">Departamento</label>
              <select
                className="form-select"
                value={filtros.departamento_id}
                onChange={(e) => setFiltros({...filtros, departamento_id: e.target.value})}
              >
                <option value="">Todos</option>
                {departamentos.map(dept => (
                  <option key={dept.id} value={dept.id}>{dept.nome}</option>
                ))}
              </select>
            </div>

            <div className="filter-item">
              <label className="form-label">Função</label>
              <select
                className="form-select"
                value={filtros.funcao_id}
                onChange={(e) => setFiltros({...filtros, funcao_id: e.target.value})}
              >
                <option value="">Todas</option>
                {funcoes.map(func => (
                  <option key={func.id} value={func.id}>{func.nome}</option>
                ))}
              </select>
            </div>

            <div className="filter-item">
              <label className="form-label">Unidade</label>
              <select
                className="form-select"
                value={filtros.unidade_id}
                onChange={(e) => setFiltros({...filtros, unidade_id: e.target.value})}
              >
                <option value="">Todas</option>
                {unidades.map(unid => (
                  <option key={unid.id} value={unid.id}>{unid.nome}</option>
                ))}
              </select>
            </div>
          </div>

          <div style={{display: 'flex', gap: '0.5rem', alignItems: 'end'}}>
            <button className="btn btn-outline btn-small" onClick={clearFilters}>
              Limpar
            </button>
            {onAdd && (
              <button className="btn btn-primary btn-small" onClick={onAdd}>
                + Adicionar
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="cards-grid">
        {funcionarios.map(funcionario => (
          <FuncionarioCard
            key={funcionario.id}
            funcionario={funcionario}
            onEdit={onEdit}
            onDelete={onDelete}
          />
        ))}
      </div>

      {funcionarios.length === 0 && (
        <div style={{textAlign: 'center', padding: '2rem', color: '#64748b'}}>
          Nenhum funcionário encontrado
        </div>
      )}
    </>
  )
}

// Componente do card de funcionário
function FuncionarioCard({ funcionario, onEdit, onDelete }) {
  const handleEmailClick = () => {
    if (funcionario.email) {
      window.open(`mailto:${funcionario.email}`, '_blank')
    }
  }

  const handleRamalClick = () => {
    if (funcionario.ramal) {
      window.open(`https://www.microsip.org/`, '_blank')
    }
  }

  const handleWhatsAppClick = () => {
    if (funcionario.whatsapp) {
      const numero = funcionario.whatsapp.replace(/\D/g, '')
      window.open(`https://wa.me/55${numero}`, '_blank')
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <div>
          <h3 className="card-title">{funcionario.nome}</h3>
          {funcionario.unidade && (
            <span className={`badge ${funcionario.unidade.toLowerCase().includes('chiaperini') ? 'badge-chiaperini' : 'badge-techto'}`}>
              {funcionario.unidade}
            </span>
          )}
        </div>
        {(onEdit || onDelete) && (
          <div className="card-actions">
            {onEdit && (
              <button className="btn btn-outline btn-small" onClick={() => onEdit(funcionario)}>
                ✏️
              </button>
            )}
            {onDelete && (
              <button className="btn btn-danger btn-small" onClick={() => onDelete(funcionario.id)}>
                🗑️
              </button>
            )}
          </div>
        )}
      </div>

      <div className="card-info">
        {funcionario.departamento && (
          <div className="info-item">
            <span className="info-label">Depto:</span>
            <span className="info-value">{funcionario.departamento}</span>
          </div>
        )}
        
        {funcionario.funcao && (
          <div className="info-item">
            <span className="info-label">Função:</span>
            <span className="info-value">{funcionario.funcao}</span>
          </div>
        )}

        {funcionario.ramal && (
          <div className="info-item">
            <span className="info-label">Ramal:</span>
            <button className="btn btn-outline btn-small" onClick={handleRamalClick}>
              📞 {funcionario.ramal}
            </button>
          </div>
        )}

        {funcionario.email && (
          <div className="info-item">
            <span className="info-label">Email:</span>
            <button className="btn btn-outline btn-small" onClick={handleEmailClick}>
              📧 {funcionario.email}
            </button>
          </div>
        )}

        {funcionario.whatsapp && (
          <div className="info-item">
            <span className="info-label">WhatsApp:</span>
            <button className="btn btn-success btn-small" onClick={handleWhatsAppClick}>
              💬 {funcionario.whatsapp}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

// Componente do formulário de funcionário
function FuncionarioForm({ formData, setFormData, departamentos, funcoes, unidades }) {
  return (
    <>
      <div className="form-group">
        <label className="form-label">Nome *</label>
        <input
          type="text"
          className="form-input"
          value={formData.nome || ''}
          onChange={(e) => setFormData({...formData, nome: e.target.value})}
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label">Ramal</label>
        <input
          type="text"
          className="form-input"
          value={formData.ramal || ''}
          onChange={(e) => setFormData({...formData, ramal: e.target.value})}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Email</label>
        <input
          type="email"
          className="form-input"
          value={formData.email || ''}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
        />
      </div>

      <div className="form-group">
        <label className="form-label">WhatsApp</label>
        <input
          type="text"
          className="form-input"
          placeholder="(11) 99999-9999"
          value={formData.whatsapp || ''}
          onChange={(e) => setFormData({...formData, whatsapp: e.target.value})}
        />
      </div>

      <div className="form-group">
        <label className="form-label">Departamento</label>
        <select
          className="form-select"
          value={formData.departamento_id || ''}
          onChange={(e) => setFormData({...formData, departamento_id: e.target.value})}
        >
          <option value="">Selecione...</option>
          {departamentos.map(dept => (
            <option key={dept.id} value={dept.id}>{dept.nome}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label className="form-label">Função</label>
        <select
          className="form-select"
          value={formData.funcao_id || ''}
          onChange={(e) => setFormData({...formData, funcao_id: e.target.value})}
        >
          <option value="">Selecione...</option>
          {funcoes.map(func => (
            <option key={func.id} value={func.id}>{func.nome}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label className="form-label">Unidade</label>
        <select
          className="form-select"
          value={formData.unidade_id || ''}
          onChange={(e) => setFormData({...formData, unidade_id: e.target.value})}
        >
          <option value="">Selecione...</option>
          {unidades.map(unid => (
            <option key={unid.id} value={unid.id}>{unid.nome}</option>
          ))}
        </select>
      </div>
    </>
  )
}

// Componente da aba Configurações
function ConfiguracoesTab({ departamentos, funcoes, unidades, onEdit, onDelete, onAdd }) {
  const [activeConfig, setActiveConfig] = useState('departamentos')

  const configs = {
    departamentos: { title: 'Departamentos', data: departamentos },
    funcoes: { title: 'Funções', data: funcoes },
    unidades: { title: 'Unidades', data: unidades }
  }

  return (
    <>
      <div className="nav-tabs">
        {Object.entries(configs).map(([key, config]) => (
          <button
            key={key}
            className={`nav-tab ${activeConfig === key ? 'active' : ''}`}
            onClick={() => setActiveConfig(key)}
          >
            {config.title}
          </button>
        ))}
      </div>

      <div style={{marginBottom: '1rem'}}>
        <button className="btn btn-primary" onClick={() => onAdd(activeConfig.slice(0, -1))}>
          + Adicionar {configs[activeConfig].title.slice(0, -1)}
        </button>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {configs[activeConfig].data.map(item => (
              <tr key={item.id}>
                <td>{item.nome}</td>
                <td>
                  <div style={{display: 'flex', gap: '0.5rem'}}>
                    <button 
                      className="btn btn-outline btn-small"
                      onClick={() => onEdit(activeConfig.slice(0, -1), item)}
                    >
                      ✏️ Editar
                    </button>
                    <button 
                      className="btn btn-danger btn-small"
                      onClick={() => onDelete(activeConfig.slice(0, -1), item.id)}
                    >
                      🗑️ Excluir
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {configs[activeConfig].data.length === 0 && (
        <div style={{textAlign: 'center', padding: '2rem', color: '#64748b'}}>
          Nenhum item encontrado
        </div>
      )}
    </>
  )
}

// Componente Modal
function Modal({ title, children, onClose }) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title">{title}</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        {children}
      </div>
    </div>
  )
}

export default App

