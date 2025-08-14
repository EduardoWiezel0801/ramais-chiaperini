import { useState } from 'react'
import Layout from '../components/layout/Layout'
import Modal from '../components/common/Modal'
import FuncionariosTab from '../components/funcionarios/FuncionariosTab'
import FuncionarioForm from '../components/funcionarios/FuncionarioForm'
import ConfiguracoesTab from '../components/configuracoes/ConfiguracoesTab'
import { useFuncionarios } from '../hooks/useFuncionarios'

function Dashboard({ user, onLogout, message, clearMessage, showMessage }) {
  const [activeTab, setActiveTab] = useState('funcionarios')
  
  // Estados para modais
  const [showModal, setShowModal] = useState(false)
  const [modalType, setModalType] = useState('')
  const [editingItem, setEditingItem] = useState(null)
  const [formData, setFormData] = useState({})

  // Hook para gerenciar funcionários e dados relacionados
  const {
    funcionarios,
    departamentos,
    funcoes,
    unidades,
    busca,
    setBusca,
    filtros,
    setFiltros,
    clearFilters,
    createFuncionario,
    updateFuncionario,
    deleteFuncionario,
    createDepartamento,
    updateDepartamento,
    deleteDepartamento,
    createFuncao,
    updateFuncao,
    deleteFuncao,
    createUnidade,
    updateUnidade,
    deleteUnidade
  } = useFuncionarios()

  // Funções para modais
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

  // Função genérica para salvar itens
  const saveItem = async () => {
    try {
      let result
      
      if (modalType === 'funcionario') {
        result = editingItem 
          ? await updateFuncionario(editingItem.id, formData)
          : await createFuncionario(formData)
      } else if (modalType === 'departamento') {
        result = editingItem 
          ? await updateDepartamento(editingItem.id, formData)
          : await createDepartamento(formData)
      } else if (modalType === 'funcao') {
        result = editingItem 
          ? await updateFuncao(editingItem.id, formData)
          : await createFuncao(formData)
      } else if (modalType === 'unidade') {
        result = editingItem 
          ? await updateUnidade(editingItem.id, formData)
          : await createUnidade(formData)
      }

      if (result.success) {
        showMessage('success', `${modalType} ${editingItem ? 'atualizado' : 'criado'} com sucesso!`)
        closeModal()
      } else {
        showMessage('error', result.message)
      }
    } catch (error) {
      showMessage('error', 'Erro de conexão')
      console.error('Erro ao salvar:', error)
    }
  }

  // Função genérica para deletar itens
  const deleteItem = async (type, id) => {
    if (!confirm('Tem certeza que deseja excluir?')) return

    try {
      let result
      
      if (type === 'funcionario') {
        result = await deleteFuncionario(id)
      } else if (type === 'departamento') {
        result = await deleteDepartamento(id)
      } else if (type === 'funcao') {
        result = await deleteFuncao(id)
      } else if (type === 'unidade') {
        result = await deleteUnidade(id)
      }

      if (result.success) {
        showMessage('success', `${type} excluído com sucesso!`)
      } else {
        showMessage('error', result.message)
      }
    } catch (error) {
      showMessage('error', 'Erro de conexão')
      console.error('Erro ao excluir:', error)
    }
  }

  const getModalTitle = () => {
    const titles = {
      funcionario: 'Funcionário',
      departamento: 'Departamento',
      funcao: 'Função',
      unidade: 'Unidade'
    }
    return `${editingItem ? 'Editar' : 'Adicionar'} ${titles[modalType]}`
  }

  return (
    <Layout 
      user={user} 
      onLogout={onLogout} 
      message={message} 
      clearMessage={clearMessage}
    >
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
        <Modal title={getModalTitle()} onClose={closeModal}>
          {modalType === 'funcionario' ? (
            <FuncionarioForm
              formData={formData}
              setFormData={setFormData}
              departamentos={departamentos}
              funcoes={funcoes}
              unidades={unidades}
              onSubmit={saveItem}
              onCancel={closeModal}
              isEditing={!!editingItem}
            />
          ) : (
            <div className="modal-body">
              <form onSubmit={(e) => { e.preventDefault(); saveItem(); }}>
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
          )}
        </Modal>
      )}
    </Layout>
  )
}

export default Dashboard