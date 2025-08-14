function FuncionarioForm({ 
  formData, 
  setFormData, 
  departamentos, 
  funcoes, 
  unidades,
  onSubmit,
  onCancel,
  isEditing = false
}) {
  const handleSubmit = (e) => {
    e.preventDefault()
    onSubmit()
  }

  return (
    <div className="modal-body">
      <form onSubmit={handleSubmit}>
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
          <label className="form-label">WhatsApp</label>
          <input
            type="text"
            className="form-input"
            value={formData.whatsapp || ''}
            onChange={(e) => setFormData({...formData, whatsapp: e.target.value})}
            placeholder="(11) 99999-9999"
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

        <div className="modal-footer">
          <button type="button" className="btn btn-outline" onClick={onCancel}>
            Cancelar
          </button>
          <button type="submit" className="btn btn-primary">
            {isEditing ? 'Atualizar' : 'Criar'}
          </button>
        </div>
      </form>
    </div>
  )
}

export default FuncionarioForm