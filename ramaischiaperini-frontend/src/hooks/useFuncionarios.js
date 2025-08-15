import { useState, useEffect } from 'react'
import { 
  funcionarioService, 
  departamentoService, 
  funcaoService, 
  unidadeService 
} from '../services/api'

export function useFuncionarios() {
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

  // Carregar todos os dados
  const loadAllData = async () => {
    try {
      // Construir parâmetros de busca - apenas incluir se não estiverem vazios
      const queryParams = {}
      
      if (busca.trim()) {
        queryParams.busca = busca.trim()
      }
      
      if (filtros.departamento_id) {
        queryParams.departamento_id = filtros.departamento_id
      }
      
      if (filtros.funcao_id) {
        queryParams.funcao_id = filtros.funcao_id
      }
      
      if (filtros.unidade_id) {
        queryParams.unidade_id = filtros.unidade_id
      }

      const [funcData, deptData, funcaoData, unidData] = await Promise.all([
        funcionarioService.getAll(queryParams),
        departamentoService.getAll(),
        funcaoService.getAll(),
        unidadeService.getAll()
      ])

      setFuncionarios(funcData)
      setDepartamentos(deptData)
      setFuncoes(funcaoData)
      setUnidades(unidData)
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
      throw new Error('Erro ao carregar dados')
    }
  }

  // Recarregar dados quando filtros mudarem
  useEffect(() => {
    loadAllData()
  }, [busca, filtros])

  const clearFilters = () => {
    setBusca('')
    setFiltros({ departamento_id: '', funcao_id: '', unidade_id: '' })
  }

  // CRUD Funcionários
  const createFuncionario = async (data) => {
    // Garantir que os IDs sejam enviados corretamente
    const payload = {
      nome: data.nome,
      email: data.email || '',
      ramal: data.ramal || '',
      whatsapp: data.whatsapp || '',
      departamento: data.departamento || data.departamento_id,
      funcao: data.funcao || data.funcao_id,
      unidade: data.unidade || data.unidade_id
    }

    const response = await funcionarioService.create(payload)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao salvar' }))
      const errorMessage = Object.values(errorData).flat().join(', ') || 'Erro ao salvar'
      return { success: false, message: errorMessage }
    }
  }

  const updateFuncionario = async (id, data) => {
    // Garantir que os IDs sejam enviados corretamente
    const payload = {
      nome: data.nome,
      email: data.email || '',
      ramal: data.ramal || '',
      whatsapp: data.whatsapp || '',
      departamento: data.departamento || data.departamento_id,
      funcao: data.funcao || data.funcao_id,
      unidade: data.unidade || data.unidade_id
    }

    const response = await funcionarioService.update(id, payload)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao atualizar' }))
      const errorMessage = Object.values(errorData).flat().join(', ') || 'Erro ao atualizar'
      return { success: false, message: errorMessage }
    }
  }

  const deleteFuncionario = async (id) => {
    const response = await funcionarioService.delete(id)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao excluir' }))
      return { success: false, message: errorData.detail || 'Erro ao excluir' }
    }
  }

  // CRUD Departamentos
  const createDepartamento = async (data) => {
    const response = await departamentoService.create(data)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao salvar' }))
      const errorMessage = Object.values(errorData).flat().join(', ') || 'Erro ao salvar'
      return { success: false, message: errorMessage }
    }
  }

  const updateDepartamento = async (id, data) => {
    const response = await departamentoService.update(id, data)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao atualizar' }))
      const errorMessage = Object.values(errorData).flat().join(', ') || 'Erro ao atualizar'
      return { success: false, message: errorMessage }
    }
  }

  const deleteDepartamento = async (id) => {
    const response = await departamentoService.delete(id)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao excluir' }))
      return { success: false, message: errorData.detail || 'Erro ao excluir' }
    }
  }

  // CRUD Funções
  const createFuncao = async (data) => {
    const response = await funcaoService.create(data)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao salvar' }))
      const errorMessage = Object.values(errorData).flat().join(', ') || 'Erro ao salvar'
      return { success: false, message: errorMessage }
    }
  }

  const updateFuncao = async (id, data) => {
    const response = await funcaoService.update(id, data)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao atualizar' }))
      const errorMessage = Object.values(errorData).flat().join(', ') || 'Erro ao atualizar'
      return { success: false, message: errorMessage }
    }
  }

  const deleteFuncao = async (id) => {
    const response = await funcaoService.delete(id)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao excluir' }))
      return { success: false, message: errorData.detail || 'Erro ao excluir' }
    }
  }

  // CRUD Unidades
  const createUnidade = async (data) => {
    const response = await unidadeService.create(data)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao salvar' }))
      const errorMessage = Object.values(errorData).flat().join(', ') || 'Erro ao salvar'
      return { success: false, message: errorMessage }
    }
  }

  const updateUnidade = async (id, data) => {
    const response = await unidadeService.update(id, data)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao atualizar' }))
      const errorMessage = Object.values(errorData).flat().join(', ') || 'Erro ao atualizar'
      return { success: false, message: errorMessage }
    }
  }

  const deleteUnidade = async (id) => {
    const response = await unidadeService.delete(id)
    if (response.ok) {
      await loadAllData()
      return { success: true }
    } else {
      const errorData = await response.json().catch(() => ({ detail: 'Erro ao excluir' }))
      return { success: false, message: errorData.detail || 'Erro ao excluir' }
    }
  }

  return {
    // Estados
    funcionarios,
    departamentos,
    funcoes,
    unidades,
    busca,
    setBusca,
    filtros,
    setFiltros,
    
    // Funções
    loadAllData,
    clearFilters,
    
    // CRUD Funcionários
    createFuncionario,
    updateFuncionario,
    deleteFuncionario,
    
    // CRUD Departamentos
    createDepartamento,
    updateDepartamento,
    deleteDepartamento,
    
    // CRUD Funções
    createFuncao,
    updateFuncao,
    deleteFuncao,
    
    // CRUD Unidades
    createUnidade,
    updateUnidade,
    deleteUnidade
  }
}