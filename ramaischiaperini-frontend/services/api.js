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
export const authenticatedFetch = async (url, options = {}) => {
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

// Serviços de API
export const authService = {
  async checkAuth() {
    const response = await authenticatedFetch(`${API_BASE}/auth/me/`)
    if (response.ok) {
      return await response.json()
    }
    return null
  },

  async login(username, password) {
    const response = await authenticatedFetch(`${API_BASE}/auth/login/`, {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
    return { response, data: await response.json().catch(() => ({})) }
  },

  async logout() {
    return await authenticatedFetch(`${API_BASE}/auth/logout/`, {
      method: 'POST'
    })
  }
}

export const funcionarioService = {
  async getAll(params = {}) {
    const queryParams = new URLSearchParams(params)
    const response = await authenticatedFetch(`${API_BASE}/funcionarios/?${queryParams}`)
    if (response.ok) {
      const data = await response.json()
      return Array.isArray(data) ? data : data.results || []
    }
    return []
  },

  async create(data) {
    return await authenticatedFetch(`${API_BASE}/funcionarios/`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },

  async update(id, data) {
    return await authenticatedFetch(`${API_BASE}/funcionarios/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  },

  async delete(id) {
    return await authenticatedFetch(`${API_BASE}/funcionarios/${id}/`, {
      method: 'DELETE'
    })
  }
}

export const departamentoService = {
  async getAll() {
    const response = await authenticatedFetch(`${API_BASE}/departamentos/`)
    if (response.ok) {
      const data = await response.json()
      return Array.isArray(data) ? data : data.results || []
    }
    return []
  },

  async create(data) {
    return await authenticatedFetch(`${API_BASE}/departamentos/`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },

  async update(id, data) {
    return await authenticatedFetch(`${API_BASE}/departamentos/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  },

  async delete(id) {
    return await authenticatedFetch(`${API_BASE}/departamentos/${id}/`, {
      method: 'DELETE'
    })
  }
}

export const funcaoService = {
  async getAll() {
    const response = await authenticatedFetch(`${API_BASE}/funcoes/`)
    if (response.ok) {
      const data = await response.json()
      return Array.isArray(data) ? data : data.results || []
    }
    return []
  },

  async create(data) {
    return await authenticatedFetch(`${API_BASE}/funcoes/`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },

  async update(id, data) {
    return await authenticatedFetch(`${API_BASE}/funcoes/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  },

  async delete(id) {
    return await authenticatedFetch(`${API_BASE}/funcoes/${id}/`, {
      method: 'DELETE'
    })
  }
}

export const unidadeService = {
  async getAll() {
    const response = await authenticatedFetch(`${API_BASE}/unidades/`)
    if (response.ok) {
      const data = await response.json()
      return Array.isArray(data) ? data : data.results || []
    }
    return []
  },

  async create(data) {
    return await authenticatedFetch(`${API_BASE}/unidades/`, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  },

  async update(id, data) {
    return await authenticatedFetch(`${API_BASE}/unidades/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  },

  async delete(id) {
    return await authenticatedFetch(`${API_BASE}/unidades/${id}/`, {
      method: 'DELETE'
    })
  }
}