import { useState } from 'react'

function ConfiguracoesTab({ 
  departamentos, 
  funcoes, 
  unidades, 
  onEdit, 
  onDelete, 
  onAdd,
  user
}) {
  const [activeConfig, setActiveConfig] = useState('departamentos')

  // Verificar se usuário pode editar
  const canEdit = user.is_admin || user.can_edit;

  const configs = {
    departamentos: { title: 'Departamentos', data: departamentos },
    funcoes: { title: 'Funções', data: funcoes },
    unidades: { title: 'Unidades', data: unidades }
  }

  const handleDelete = async (type, id) => {
    if (!confirm('Tem certeza que deseja excluir?')) return
    await onDelete(type, id)
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

      <div style={{marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <h2>{configs[activeConfig].title} ({configs[activeConfig].data.length})</h2>
        {canEdit && (
          <button 
            className="btn btn-primary" 
            onClick={() => onAdd(activeConfig.slice(0, -1))}
          >
            + Adicionar {configs[activeConfig].title.slice(0, -1)}
          </button>
        )}
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Colaboradores</th>
              {canEdit && <th>Ações</th>}
            </tr>
          </thead>
          <tbody>
            {configs[activeConfig].data.map(item => (
              <tr key={item.id}>
                <td>{item.nome}</td>
                <td>
                  <span className="badge badge-chiaperini">
                    {item.funcionarios_count || 0}
                  </span>
                </td>
                {canEdit && (
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
                        onClick={() => handleDelete(activeConfig.slice(0, -1), item.id)}
                      >
                        🗑️ Excluir
                      </button>
                    </div>
                  </td>
                )}
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

export default ConfiguracoesTab