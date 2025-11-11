import { createI18n } from 'vue-i18n'

// Safe localStorage access
const safeGetLocaleStorage = () => {
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      return localStorage.getItem('locale')
    }
  } catch (err) {
    console.warn('localStorage not available:', err.message)
  }
  return null
}

const safeSetLocaleStorage = (locale) => {
  try {
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.setItem('locale', locale)
    }
  } catch (err) {
    console.warn('localStorage not available:', err.message)
  }
}

// Detect user's language preference
const getLocale = () => {
  // Check localStorage first
  const saved = safeGetLocaleStorage()
  if (saved) return saved

  // Check browser language
  try {
    const browserLang = navigator.language || navigator.userLanguage
    
    // Map browser language to supported locales
    if (browserLang.startsWith('pt')) {
      return 'pt-BR'
    }
    if (browserLang.startsWith('en')) {
      return 'en-US'
    }
  } catch (err) {
    console.warn('Browser language detection failed:', err.message)
  }

  // Default to English
  return 'en-US'
}

// Load namespace messages dynamically (lazy loading support)
const loadMessages = async (locale) => {
  const namespaces = ['common', 'navigation', 'events', 'players', 'matches', 'ranking', 'validation', 'messages', 'settings']
  const messages = {}
  
  for (const namespace of namespaces) {
    try {
      // Dynamically import namespace files
      const module = await import(`./locales/${locale}/${namespace}.json`)
      messages[namespace] = module.default
    } catch (err) {
      console.warn(`Failed to load namespace ${namespace} for ${locale}:`, err.message)
    }
  }
  
  return messages
}

// Initialize i18n with bundled common messages (most frequent)
const initializeI18n = async () => {
  // Import only the common namespace for immediate loading
  const ptBRCommon = await import('./locales/pt-BR/common.json')
  const enUSCommon = await import('./locales/en-US/common.json')
  
  const locale = getLocale()
  
  // Create i18n instance with minimal messages first
  const i18n = createI18n({
    legacy: false,
    locale: locale,
    fallbackLocale: 'en-US',
    messages: {
      'pt-BR': ptBRCommon.default,
      'en-US': enUSCommon.default
    },
    globalInjection: true,
    missingWarn: false,
    fallbackWarn: false
  })
  
  // Load remaining namespaces in background (lazy)
  const loadAllNamespaces = async () => {
    const ptBRMessages = await loadMessages('pt-BR')
    const enUSMessages = await loadMessages('en-US')
    
    // Merge into i18n
    i18n.global.setLocaleMessage('pt-BR', ptBRMessages)
    i18n.global.setLocaleMessage('en-US', enUSMessages)
  }
  
  // Start loading but don't wait (non-blocking)
  loadAllNamespaces().catch(err => {
    console.error('Failed to load all namespaces:', err)
  })
  
  return i18n
}

// Create i18n promise
let i18nPromise = initializeI18n()

// Export function to change locale
export const setLocale = async (locale) => {
  const i18n = await i18nPromise
  i18n.global.locale.value = locale
  safeSetLocaleStorage(locale)
  
  // Load all namespaces for new locale if not already loaded
  const messages = await loadMessages(locale)
  i18n.global.setLocaleMessage(locale, messages)
}

// Export function to get available locales
export const getAvailableLocales = () => [
  { code: 'pt-BR', name: 'Português (BR)' },
  { code: 'en-US', name: 'English (US)' }
]

// Default export resolves the i18n promise
export default i18nPromise
