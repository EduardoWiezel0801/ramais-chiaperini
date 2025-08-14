import { useState, useEffect } from 'react'
import './App.css'

const API_BASE = 'http://localhost:8000/api'

// Função para obter CSRF token
const getCSRFToken = () => {
  const name = 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Função para fazer requisições autenticadas
const authenticatedFetch = async (url, options = {}) => {
  const csrfToken = getCSRFToken()
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken || '',
  }

  const config = {
    credentials: 'include',
    headers: { ...defaultHeaders, ...options.headers },
    ...options
  }

  return fetch(url, config)
}

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
  const [modalType, setModalType] = useState('')
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({})
  
  // Estados para mensagens
  const [message, setMessage] = useState({ type: '', text: '' })

  // Verificar autenticação ao carregar
  useEffect(() => {
    initializeApp()
  }, [])

  // Carregar dados quando usuário logado
  useEffect(() => {
    if (user) {
      loadAllData()
    }
  }, [user])

  // Recarregar dados quando filtros mudarem
  useEffect(() => {
    if (user) {
      loadAllData()
    }
  }, [busca, filtros])

  const initializeApp = async () => {
    try {
      // Primeiro, obter CSRF token fazendo uma requisição inicial
      await authenticatedFetch(`${API_BASE}/`)
      
      // Depois verificar autenticação
      await checkAuth()
    } catch (error) {
      console.error('Erro ao inicializar app:', error)
    } finally {
      setLoading(false)
    }
  }

  const checkAuth = async () => {
    try {
      const response = await authenticatedFetch(`${API_BASE}/auth/me/`)
      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
      }
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error)
    }
  }

  const loadAllData = async () => {
    try {
      const queryParams = new URLSearchParams({
        busca: busca || '',
        departamento_id: filtros.departamento_id || '',
        funcao_id: filtros.funcao_id || '',
        unidade_id: filtros.unidade_id || ''
      })

      const [funcRes, deptRes, funcaoRes, unidRes] = await Promise.all([
        authenticatedFetch(`${API_BASE}/funcionarios/?${queryParams}`),
        authenticatedFetch(`${API_BASE}/departamentos/`),
        authenticatedFetch(`${API_BASE}/funcoes/`),
        authenticatedFetch(`${API_BASE}/unidades/`)
      ])

      if (funcRes.ok) {
        const funcData = await funcRes.json()
        setFuncionarios(Array.isArray(funcData) ? funcData : funcData.results || [])
      }
      if (deptRes.ok) {
        const deptData = await deptRes.json()
        setDepartamentos(Array.isArray(deptData) ? deptData : deptData.results || [])
      }
      if (funcaoRes.ok) {
        const funcaoData = await funcaoRes.json()
        setFuncoes(Array.isArray(funcaoData) ? funcaoData : funcaoData.results || [])
      }
      if (unidRes.ok) {
        const unidData = await unidRes.json()
        setUnidades(Array.isArray(unidData) ? unidData : unidData.results || [])
      }
    } catch (error) {
      showMessage('error', 'Erro ao carregar dados')
      console.error('Erro ao carregar dados:', error)
    }
  }

  const login = async (username, password) => {
    try {
      const response = await authenticatedFetch(`${API_BASE}/auth/login/`, {
        method: 'POST',
        body: JSON.stringify({ username, password })
      })

      if (response.ok) {
        const data = await response.json()
        setUser(data.user)
        showMessage('success', 'Login realizado com sucesso!')
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Erro no login' }))
        showMessage('error', errorData.detail || errorData.username?.[0] || errorData.password?.[0] || 'Erro no login')
      }
    } catch (error) {
      showMessage('error', 'Erro de conexão')
      console.error('Erro no login:', error)
    }
  }

  const logout = async () => {
    try {
      await authenticatedFetch(`${API_BASE}/auth/logout/`, {
        method: 'POST'
      })
      setUser(null)
      setFuncionarios([])
      setDepartamentos([])
      setFuncoes([])
      setUnidades([])
      showMessage('success', 'Logout realizado com sucesso!')
    } catch (error) {
      showMessage('error', 'Erro no logout')
      console.error('Erro no logout:', error)
    }
  }

  const showMessage = (type, text) => {
    setMessage({ type, text })
    setTimeout(() => setMessage({ type: '', text: '' }), 5000)
  }

  const clearFilters = () => {
    setBusca('')
    setFiltros({ departamento_id: '', funcao_id: '', unidade_id: '' })
  }

  // Funções CRUD
  const saveItem = async () => {
    try {
      const url = editingItem 
        ? `${API_BASE}/${modalType}s/${editingItem.id}/`
        : `${API_BASE}/${modalType}s/`
      
      const response = await authenticatedFetch(url, {
        method: editingItem ? 'PUT' : 'POST',
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        showMessage('success', `${modalType} ${editingItem ? 'atualizado' : 'criado'} com sucesso!`)
        setShowModal(false)
        setEditingItem(null)
        setFormData({})
        loadAllData()
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Erro ao salvar' }))
        const errorMessage = Object.values(errorData).flat().join(', ') || 'Erro ao salvar'
        showMessage('error', errorMessage)
      }
    } catch (error) {
      showMessage('error', 'Erro de conexão')
      console.error('Erro ao salvar:', error)
    }
  }

  const deleteItem = async (type, id) => {
    if (!confirm('Tem certeza que deseja excluir?')) return

    try {
      const response = await authenticatedFetch(`${API_BASE}/${type}s/${id}/`, {
        method: 'DELETE'
      })

      if (response.ok) {
        showMessage('success', `${type} excluído com sucesso!`)
        loadAllData()
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Erro ao excluir' }))
        showMessage('error', errorData.detail || 'Erro ao excluir')
      }
    } catch (error) {
      showMessage('error', 'Erro de conexão')
      console.error('Erro ao excluir:', error)
    }
  }

  const openModal = (type, item = null) => {
    setModalType(type)
    setEditingItem(item)
    setFormData(item || {})
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setEditingItem(null)
    setFormData({})
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading">Carregando...</div>
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
          <h1 className="logo">Sistema de Ramais - Chiaperini</h1>
          <div className="user-info">
            <span className="user-name">Olá, {user.username}</span>
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

        <div className="nav-tabs">
          <button
            className={`nav-tab ${activeTab === 'funcionarios' ? 'active' : ''}`}
            onClick={() => setActiveTab('funcionarios')}
          >
            👥 Funcionários
          </button>
          <button
            className={`nav-tab ${activeTab === 'configuracoes' ? 'active' : ''}`}
            onClick={() => setActiveTab('configuracoes')}
          >
            ⚙️ Configurações
          </button>
        </div>

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
            onEdit={(item) => openModal('funcionario', item)}
            onDelete={(id) => deleteItem('funcionario', id)}
            onAdd={() => openModal('funcionario')}
          />
        )}

        {activeTab === 'configuracoes' && (
          <ConfiguracoesTab
            departamentos={departamentos}
            funcoes={funcoes}
            unidades={unidades}
            onEdit={(type, item) => openModal(type, item)}
            onDelete={deleteItem}
            onAdd={(type) => openModal(type)}
          />
        )}

        {showModal && (
          <Modal
            title={`${editingItem ? 'Editar' : 'Adicionar'} ${
              modalType === 'funcionario' ? 'Funcionário' : 
              modalType === 'departamento' ? 'Departamento' :
              modalType === 'funcao' ? 'Função' : 'Unidade'
            }`}
            onClose={closeModal}
          >
            <div className="modal-body">
              <form onSubmit={(e) => { e.preventDefault(); saveItem(); }}>
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

                <div className="modal-footer">
                  <button type="button" className="btn btn-outline" onClick={closeModal}>
                    Cancelar
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {editingItem ? 'Atualizar' : 'Criar'}
                  </button>
                </div>
              </form>
            </div>
          </Modal>
        )}
      </main>
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
      <div className="filters-section">
        <div className="search-box">
          <input
            type="text"
            className="form-input"
            placeholder="🔍 Buscar funcionário..."
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
          />
        </div>

        <div className="filters-grid">
          <select
            className="form-select"
            value={filtros.departamento_id}
            onChange={(e) => setFiltros({...filtros, departamento_id: e.target.value})}
          >
            <option value="">Todos os departamentos</option>
            {departamentos.map(dept => (
              <option key={dept.id} value={dept.id}>{dept.nome}</option>
            ))}
          </select>

          <select
            className="form-select"
            value={filtros.funcao_id}
            onChange={(e) => setFiltros({...filtros, funcao_id: e.target.value})}
          >
            <option value="">Todas as funções</option>
            {funcoes.map(func => (
              <option key={func.id} value={func.id}>{func.nome}</option>
            ))}
          </select>

          <select
            className="form-select"
            value={filtros.unidade_id}
            onChange={(e) => setFiltros({...filtros, unidade_id: e.target.value})}
          >
            <option value="">Todas as unidades</option>
            {unidades.map(unid => (
              <option key={unid.id} value={unid.id}>{unid.nome}</option>
            ))}
          </select>

          <button className="btn btn-outline" onClick={clearFilters}>
            🗑️ Limpar Filtros
          </button>
        </div>
      </div>

      <div className="actions-bar">
        <button className="btn btn-primary" onClick={onAdd}>
          + Adicionar Funcionário
        </button>
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Ramal</th>
              <th>Departamento</th>
              <th>Função</th>
              <th>Unidade</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {funcionarios.map(func => (
              <tr key={func.id}>
                <td>
                  <div className="employee-info">
                    <div className="employee-name">{func.nome}</div>
                    <div className="employee-details">
                      <span className="info-item">
                        <span className="info-label">📧</span>
                        <span className="info-value">{func.email}</span>
                      </span>
                    </div>
                  </div>
                </td>
                <td>
                  <div className="ramal-info">
                    <span className="ramal-number">{func.ramal}</span>
                  </div>
                </td>
                <td>
                  <span className={`badge badge-${func.departamento_nome === 'Chiaperini' ? 'chiaperini' : 'techto'}`}>
                    {func.departamento_nome || func.departamento?.nome}
                  </span>
                </td>
                <td>{func.funcao_nome || func.funcao?.nome}</td>
                <td>{func.unidade_nome || func.unidade?.nome}</td>
                <td>
                  <div style={{display: 'flex', gap: '0.5rem'}}>
                    <button 
                      className="btn btn-outline btn-small"
                      onClick={() => onEdit(func)}
                    >
                      ✏️ Editar
                    </button>
                    <button 
                      className="btn btn-danger btn-small"
                      onClick={() => onDelete(func.id)}
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

      {funcionarios.length === 0 && (
        <div style={{textAlign: 'center', padding: '2rem', color: '#64748b'}}>
          Nenhum funcionário encontrado
        </div>
      )}
    </>
  )
}

// Componente do formulário de funcionário
function FuncionarioForm({ formData, setFormData, departamentos, funcoes, unidades }) {
  return (
    <>
      <div className="form-group">
        <label className="form-label">Nome Completo</label>
        <input
          type="text"
          className="form-input"
          value={formData.nome || ''}
          onChange={(e) => setFormData({...formData, nome: e.target.value})}
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label">Email</label>
        <input
          type="email"
          className="form-input"
          value={formData.email || ''}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
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
          required
        />
      </div>

      <div className="form-group">
        <label className="form-label">Departamento</label>
        <select
          className="form-select"
          value={formData.departamento_id || formData.departamento || ''}
          onChange={(e) => setFormData({...formData, departamento_id: e.target.value})}
          required
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
          value={formData.funcao_id || formData.funcao || ''}
          onChange={(e) => setFormData({...formData, funcao_id: e.target.value})}
          required
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
          value={formData.unidade_id || formData.unidade || ''}
          onChange={(e) => setFormData({...formData, unidade_id: e.target.value})}
          required
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