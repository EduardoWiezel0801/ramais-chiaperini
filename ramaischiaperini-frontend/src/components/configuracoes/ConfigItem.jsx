function ConfigItem({ item, type, onEdit, onDelete }) {
  const handleDelete = () => {
    if (confirm('Tem certeza que deseja excluir?')) {
      onDelete(type, item.id)
    }
  }

  return (
    <tr>
      <td>{item.nome}</td>
      <td>
        <span className="badge badge-chiaperini">
          {item.funcionarios_count || 0}
        </span>
      </td>
      <td>
        <div style={{display: 'flex', gap: '0.5rem'}}>
          <button 
            className="btn btn-outline btn-small"
            onClick={() => onEdit(type, item)}
          >
            ✏️ Editar
          </button>
          <button 
            className="btn btn-danger btn-small"
            onClick={handleDelete}
          >
            🗑️ Excluir
          </button>
        </div>
      </td>
    </tr>
  )
}

export default ConfigItem