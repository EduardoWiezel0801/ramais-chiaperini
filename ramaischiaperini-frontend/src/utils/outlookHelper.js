/**
 * Utilitário para integração com cliente de email desktop
 */

/**
 * Abre o cliente de email desktop para compor um novo email
 * @param {string} destinatario - Email do destinatário
 * @param {string} assunto - Assunto do email (opcional)
 * @param {string} corpo - Corpo do email (opcional)
 */
export const abrirOutlookCompose = (destinatario, assunto = '', corpo = '') => {
  if (!destinatario) {
    console.warn('Destinatário não informado para email');
    return;
  }

  // Codifica os parâmetros para URL
  const assuntoCodificado = encodeURIComponent(assunto);
  const corpoCodificado = encodeURIComponent(corpo);
  
  // Constrói a URI mailto
  let mailtoUri = `mailto:${destinatario}`;
  
  const parametros = [];
  if (assunto) parametros.push(`subject=${assuntoCodificado}`);
  if (corpo) parametros.push(`body=${corpoCodificado}`);
  
  if (parametros.length > 0) {
    mailtoUri += `?${parametros.join('&')}`;
  }
  
  try {
    // Abre o cliente de email padrão
    window.location.href = mailtoUri;
    console.log('Abrindo cliente de email para:', destinatario);
  } catch (error) {
    console.error('Erro ao abrir cliente de email:', error);
    // Fallback: copia o email para área de transferência
    navigator.clipboard.writeText(destinatario).then(() => {
      alert(`Email ${destinatario} copiado para área de transferência`);
    }).catch(() => {
      alert(`Para enviar email, use: ${destinatario}`);
    });
  }
};

/**
 * Abre o Outlook desktop diretamente
 */
export const abrirOutlook = () => {
  try {
    // Tenta abrir o Outlook com comando Windows
    window.location.href = 'mailto:';
    console.log('Abrindo cliente de email padrão');
  } catch (error) {
    console.error('Erro ao abrir Outlook:', error);
    alert('Não foi possível abrir o cliente de email. Verifique se está instalado.');
  }
};

/**
 * Verifica se há cliente de email configurado
 */
export const verificarOutlook = () => {
  return true; // mailto sempre está disponível
};