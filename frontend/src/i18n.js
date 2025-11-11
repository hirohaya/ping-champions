import { createI18n } from 'vue-i18n'
import ptBR from './locales/pt-BR.json'
import enUS from './locales/en-US.json'

// Detect user's language preference
const getLocale = () => {
  // Check localStorage first
  const saved = localStorage.getItem('locale')
  if (saved) return saved

  // Check browser language
  const browserLang = navigator.language || navigator.userLanguage
  
  // Map browser language to supported locales
  if (browserLang.startsWith('pt')) {
    return 'pt-BR'
  }
  if (browserLang.startsWith('en')) {
    return 'en-US'
  }

  // Default to English
  return 'en-US'
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
  localStorage.setItem('locale', locale)
}

// Export function to get available locales
export const getAvailableLocales = () => [
  { code: 'pt-BR', name: 'Português (BR)' },
  { code: 'en-US', name: 'English (US)' }
]

export default i18n
