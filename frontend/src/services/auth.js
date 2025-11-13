/**
 * Serviço de Autenticação
 * 
 * Gerencia:
 * - Registro de novo usuário
 * - Login de usuário
 * - Armazenamento de token JWT
 * - Logout
 * - Recuperação de dados do usuário
 */

import api from './api'

const AUTH_TOKEN_KEY = 'auth_token'
const USER_KEY = 'user_info'

// Event emitter para notificar componentes sobre mudanças de autenticação
let authChangeListeners = []

function notifyAuthChange() {
  authChangeListeners.forEach(listener => listener())
}

/**
 * Registrar novo usuário
 * @param {string} email - Email do usuário
 * @param {string} password - Senha (será hasheada no backend)
 * @param {string} name - Nome completo
 * @param {string} role - Tipo de usuário (player, organizer)
 * @returns {Promise} Token e dados do usuário
 */
export async function register(email, password, name, role = 'player') {
  try {
    const response = await api.post('/users/register', {
      email,
      password,
      name,
      role
    })

    // Salvar token e usuário
    const { access_token, user } = response.data
    setAuthToken(access_token)
    setUserInfo(user)
    notifyAuthChange()

    return {
      success: true,
      token: access_token,
      user
    }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Erro ao registrar'
    }
  }
}

/**
 * Fazer login
 * @param {string} email - Email do usuário
 * @param {string} password - Senha
 * @returns {Promise} Token e dados do usuário
 */
export async function login(email, password) {
  try {
    const response = await api.post('/users/login', {
      email,
      password
    })

    // Salvar token e usuário
    const { access_token, user } = response.data
    setAuthToken(access_token)
    setUserInfo(user)
    notifyAuthChange()

    return {
      success: true,
      token: access_token,
      user
    }
  } catch (error) {
    return {
      success: false,
      error: error.response?.data?.detail || 'Email ou senha inválidos'
    }
  }
}

/**
 * Fazer logout
 */
export function logout() {
  localStorage.removeItem(AUTH_TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  notifyAuthChange()
}

/**
 * Obter token armazenado
 * @returns {string|null} Token JWT ou null
 */
export function getAuthToken() {
  try {
    return localStorage.getItem(AUTH_TOKEN_KEY)
  } catch (err) {
    console.warn('Não foi possível acessar localStorage:', err.message)
    return null
  }
}

/**
 * Definir token no localStorage
 * @param {string} token - Token JWT
 */
export function setAuthToken(token) {
  try {
    localStorage.setItem(AUTH_TOKEN_KEY, token)
    // Atualizar header de autorização no axios
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } catch (err) {
    console.warn('Não foi possível salvar token:', err.message)
  }
}

/**
 * Obter informações do usuário autenticado
 * @returns {object|null} Dados do usuário ou null
 */
export function getUserInfo() {
  try {
    const userJson = localStorage.getItem(USER_KEY)
    return userJson ? JSON.parse(userJson) : null
  } catch (err) {
    console.warn('Não foi possível recuperar dados do usuário:', err.message)
    return null
  }
}

/**
 * Salvar informações do usuário
 * @param {object} user - Dados do usuário
 */
export function setUserInfo(user) {
  try {
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  } catch (err) {
    console.warn('Não foi possível salvar dados do usuário:', err.message)
  }
}

/**
 * Verificar se usuário está autenticado
 * @returns {boolean} True se tem token válido
 */
export function isAuthenticated() {
  return getAuthToken() !== null
}

/**
 * Verificar se usuário tem um papel específico
 * @param {string} role - Papel a verificar (admin, organizer, player)
 * @returns {boolean} True se usuário tem esse papel
 */
export function hasRole(role) {
  const user = getUserInfo()
  return user && user.role === role
}

/**
 * Verificar se usuário é admin
 * @returns {boolean}
 */
export function isAdmin() {
  return hasRole('admin')
}

/**
 * Verificar se usuário é organizador
 * @returns {boolean}
 */
export function isOrganizer() {
  return hasRole('organizer')
}

/**
 * Verificar se usuário é jogador
 * @returns {boolean}
 */
export function isPlayer() {
  return hasRole('player')
}

/**
 * Obter usuário atual
 * @returns {object|null}
 */
export function getCurrentUser() {
  return getUserInfo()
}

/**
 * Inicializar autenticação ao carregar página
 * Restaurar token do localStorage se existir
 */
export function initializeAuth() {
  const token = getAuthToken()
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  }
}

/**
 * Inscrever-se em mudanças de autenticação
 * @param {function} listener - Função a chamar quando autenticação mudar
 * @returns {function} Função para desinscrever
 */
export function onAuthChange(listener) {
  authChangeListeners.push(listener)
  
  // Retornar função para desinscrever
  return () => {
    authChangeListeners = authChangeListeners.filter(l => l !== listener)
  }
}

// Interceptor para tratar erros de autenticação
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Se receber 401, fazer logout
    if (error.response?.status === 401) {
      logout()
      // Redirecionar para login (será feito no router)
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  register,
  login,
  logout,
  getAuthToken,
  setAuthToken,
  getUserInfo,
  setUserInfo,
  isAuthenticated,
  hasRole,
  isAdmin,
  isOrganizer,
  isPlayer,
  getCurrentUser,
  initializeAuth,
  onAuthChange
}
