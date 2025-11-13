import { createI18n } from 'vue-i18n'
import ptBR from './locales/pt-BR.json'
import enUS from './locales/en-US.json'

// ===== FEATURE FLAG: Disable English translation =====
// Set to false to disable English translation and force Portuguese (pt-BR)
// Set to true to enable English translation selector
const I18N_ENABLE_ENGLISH = false
// ====================================================

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
  // If English is disabled, always use Portuguese
  if (!I18N_ENABLE_ENGLISH) {
    return 'pt-BR'
  }

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

  // Default to Portuguese when English is disabled
  return 'pt-BR'
}

const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: getLocale(),
  fallbackLocale: 'en-US',
  messages: {
    'pt-BR': ptBR,
    'en-US': enUS
  },
  globalInjection: true,
  missingWarn: false,
  fallbackWarn: false
})

// Export function to change locale
export const setLocale = (locale) => {
  i18n.global.locale.value = locale
  safeSetLocaleStorage(locale)
}

// Export function to get available locales
export const getAvailableLocales = () => {
  const locales = [
    { code: 'pt-BR', name: 'Português (BR)' }
  ]
  if (I18N_ENABLE_ENGLISH) {
    locales.push({ code: 'en-US', name: 'English (US)' })
  }
  return locales
}

export default i18n
