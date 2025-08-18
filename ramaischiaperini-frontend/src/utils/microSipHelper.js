/**
 * Utilitário para integração com MicroSIP
 */

/**
 * Inicia uma ligação através do MicroSIP
 * @param {string} ramal - Número do ramal para ligar
 */
export const iniciarLigacao = (ramal) => {
  if (!ramal) {
    console.warn('Ramal não informado para ligação');
    return;
  }

  // Remove caracteres não numéricos do ramal
  const numeroLimpo = ramal.replace(/\D/g, '');
  
  if (!numeroLimpo) {
    console.warn('Ramal inválido:', ramal);
    return;
  }

  // Cria a URI SIP para o MicroSIP
  const sipUri = `sip:${numeroLimpo}`;
  
  try {
    // Tenta abrir com protocolo SIP
    window.location.href = sipUri;
    console.log('Iniciando ligação para ramal:', numeroLimpo);
  } catch (error) {
    console.error('Erro ao iniciar ligação:', error);
    // Fallback: mostra uma mensagem para o usuário
    alert(`Para ligar para o ramal ${numeroLimpo}, abra o MicroSIP e digite: ${numeroLimpo}`);
  }
};

/**
 * Verifica se o MicroSIP está disponível (opcional)
 * Esta função pode ser expandida para detectar se o MicroSIP está instalado
 */
export const verificarMicroSip = () => {
  // Por enquanto, assume que está disponível
  // Futuramente pode ser implementada uma verificação mais robusta
  return true;
};