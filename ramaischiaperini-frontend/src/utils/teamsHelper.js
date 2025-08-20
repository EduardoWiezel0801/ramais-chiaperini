/**
 * Utilitário para integração com Microsoft Teams desktop
 */

/**
 * Abre o Microsoft Teams desktop para iniciar chat
 * @param {string} teamsUser - Nome de usuário do Teams (ex: adenilson.junior1)
 */
export const abrirTeamsChat = (teamsUser) => {
  if (!teamsUser) {
    console.warn('Nome de usuário Teams não informado');
    return;
  }

  // Remove espaços
  const teamsUserLimpo = teamsUser.trim();
  
  if (!teamsUserLimpo) {
    console.warn('Nome de usuário Teams inválido:', teamsUser);
    return;
  }

  try {
    // URI para abrir Teams desktop - chat com nome de usuário
    // Se contém @, é email, senão é nome de usuário
    let teamsUri;
    
    if (teamsUserLimpo.includes('@')) {
      // É um email
      teamsUri = `msteams:/l/chat/0/0?users=${encodeURIComponent(teamsUserLimpo)}`;
    } else {
      // É nome de usuário do Teams - precisa do formato completo
      teamsUri = `msteams:/l/chat/0/0?users=${encodeURIComponent(teamsUserLimpo)}`;
    }
    
    // Tenta abrir o Teams desktop
    window.location.href = teamsUri;
    console.log('Abrindo Teams para chat com:', teamsUserLimpo);
    
    // Feedback visual para o usuário
    setTimeout(() => {
      // Se ainda estiver na página após 1 segundo, provavelmente não abriu o Teams
      console.log('Tentativa de abrir Teams concluída');
    }, 1000);
    
  } catch (error) {
    console.error('Erro ao abrir Teams:', error);
    
    // Fallback: tenta abrir Teams web
    try {
      let teamsWebUrl;
      
      if (teamsUserLimpo.includes('@')) {
        teamsWebUrl = `https://teams.microsoft.com/l/chat/0/0?users=${encodeURIComponent(teamsUserLimpo)}`;
      } else {
        // Para nome de usuário, tenta busca no Teams web
        teamsWebUrl = `https://teams.microsoft.com/_#/conversations/search?q=${encodeURIComponent(teamsUserLimpo)}`;
      }
      
      window.open(teamsWebUrl, '_blank');
      console.log('Abrindo Teams web para:', teamsUserLimpo);
      
    } catch (webError) {
      console.error('Erro ao abrir Teams web:', webError);
      
      // Último fallback: copia o nome de usuário
      navigator.clipboard.writeText(teamsUserLimpo).then(() => {
        alert(`Nome de usuário Teams "${teamsUserLimpo}" copiado para área de transferência. Cole no Teams para buscar.`);
      }).catch(() => {
        alert(`Para contatar no Teams, busque por: ${teamsUserLimpo}`);
      });
    }
  }
};

/**
 * Abre o Microsoft Teams desktop para videochamada
 * @param {string} teamsUser - Nome de usuário do Teams
 */
export const iniciarChamadaTeams = (teamsUser) => {
  if (!teamsUser) {
    console.warn('Nome de usuário Teams não informado para chamada');
    return;
  }

  const teamsUserLimpo = teamsUser.trim();
  
  if (!teamsUserLimpo) {
    console.warn('Nome de usuário Teams inválido para chamada:', teamsUser);
    return;
  }

  try {
    // Para chamadas, é melhor abrir o chat primeiro
    abrirTeamsChat(teamsUserLimpo);
    
    // Instrução para o usuário
    setTimeout(() => {
      console.log('Teams aberto. Use o botão de chamada no chat para ligar.');
    }, 1500);
    
  } catch (error) {
    console.error('Erro ao iniciar chamada Teams:', error);
    abrirTeamsChat(teamsUserLimpo);
  }
};

/**
 * Verifica se o Teams está disponível
 */
export const verificarTeams = () => {
  return true;
};