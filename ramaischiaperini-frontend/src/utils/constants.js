// URLs da API
export const API_BASE_URL = 'http://192.168.3.174:8000/api'

// Tipos de mensagem
export const MESSAGE_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info'
}

// Configurações de timeout
export const TIMEOUTS = {
  MESSAGE: 5000,
  REQUEST: 30000
}

// Validações
export const VALIDATION = {
  MIN_PASSWORD_LENGTH: 6,
  MAX_NAME_LENGTH: 200,
  MAX_EMAIL_LENGTH: 200
}

// Máscaras para inputs
export const MASKS = {
  PHONE: '(##) #####-####',
  RAMAL: '####'
}

// Cores dos badges
export const BADGE_COLORS = {
  CHIAPERINI: 'chiaperini',
  TECHTO: 'techto',
  DEFAULT: 'default'
}