import { iniciarLigacao } from '../../utils/microSipHelper';

function FuncionariosTab({ 
  funcionarios, 
  departamentos, 
  funcoes, 
  unidades, 
  busca, 
  setBusca, 
  filtros, 
  setFiltros, 
  clearFilters, 
  onEdit, 
  onDelete, 
  onAdd,
  user
}) {

  const canEdit = user.is_admin || user.can_edit;

  return (
    <>
      <div className="search-filters">
        <div className="search-row">
          <div className="search-input">
            <input
              type="text"
              className="form-input"
              placeholder="🔍 Buscar Colaborador..."
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
            />
          </div>

          <div className="filter-group">
            <div className="filter-item">
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
            </div>

            <div className="filter-item">
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
            </div>

            <div className="filter-item">
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
            </div>

            <button className="btn btn-outline" onClick={clearFilters}>
              🗑️ Limpar
            </button>
          </div>
        </div>
      </div>

      <div style={{marginBottom: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <h2>Colaboradores ({funcionarios.length})</h2>
        {canEdit && (
          <button className="btn btn-primary" onClick={onAdd}>
            + Adicionar Colaborador
          </button>
        )}
      </div>

      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Ramal</th>
              <th>Email</th>
              <th>WhatsApp</th>
              <th>Departamento</th>
              <th>Função</th>
              <th>Unidade</th>
              {canEdit && <th>Ações</th>}
            </tr>
          </thead>
          <tbody>
            {funcionarios.map(func => (
              <tr key={func.id}>
                <td>
                  <div className="employee-name">{func.nome}</div>
                </td>
                <td>
                  {func.ramal ? (
                    <button 
                      className="ramal-clickable"
                      onClick={() => iniciarLigacao(func.ramal)}
                      title={`Ligar para ramal ${func.ramal}`}
                    >
                      {func.ramal}
                    </button>
                  ) : '-'}
                </td>
                <td>
                  {func.email ? (
                    <a href={`mailto:${func.email}`} className="info-value">
                      {func.email}
                    </a>
                  ) : '-'}
                </td>
                <td>
                  {func.whatsapp ? (
                    <a 
                      href={`https://wa.me/55${func.whatsapp.replace(/\D/g, '')}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="info-value"
                    >
                      {func.whatsapp}
                    </a>
                  ) : '-'}
                </td>
                <td>
                  {func.departamento_nome ? (
                    <span className={`badge badge-${func.departamento_nome === 'Chiaperini' ? 'chiaperini' : 'techto'}`}>
                      {func.departamento_nome}
                    </span>
                  ) : '-'}
                </td>
                <td>{func.funcao_nome || '-'}</td>
                <td>{func.unidade_nome || '-'}</td>
                {canEdit && (
                  <td >
                    <div style={{display: 'flex', justifyContent: "center", gap: '0.5rem', width: "50%"}}>
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
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {funcionarios.length === 0 && (
        <div style={{textAlign: 'center', padding: '2rem', color: '#64748b'}}>
          Nenhum Colaborador encontrado
        </div>
      )}
    </>
  )
}

export default FuncionariosTab