import { useState, useEffect } from 'react'
import { authService, authenticatedFetch } from '../services/api'

export function useAuth() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    initializeAuth()
  }, [])

  const initializeAuth = async () => {
    try {
      // Primeiro, obter CSRF token fazendo uma requisição inicial
      await authenticatedFetch('http://localhost:8000/api/')
      
      // Depois verificar autenticação
      const userData = await authService.checkAuth()
      if (userData) {
        setUser(userData)
      }
    } catch (error) {
      console.error('Erro ao inicializar autenticação:', error)
    } finally {
      setLoading(false)
    }
  }

  const login = async (username, password) => {
    try {
      const { response, data } = await authService.login(username, password)

      if (response.ok) {
        setUser(data.user)
        return { success: true, message: 'Login realizado com sucesso!' }
      } else {
        const errorMessage = data.detail || data.username?.[0] || data.password?.[0] || 'Erro no login'
        return { success: false, message: errorMessage }
      }
    } catch (error) {
      console.error('Erro no login:', error)
      return { success: false, message: 'Erro de conexão' }
    }
  }

  const logout = async () => {
    try {
      await authService.logout()
      setUser(null)
      return { success: true, message: 'Logout realizado com sucesso!' }
    } catch (error) {
      console.error('Erro no logout:', error)
      return { success: false, message: 'Erro no logout' }
    }
  }

  return {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user
  }
}