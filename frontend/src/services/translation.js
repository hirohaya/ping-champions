/**
 * Service for fetching backend-provided localized messages
 * Optional: provides an alternative to hardcoded translations
 */

import api from './api'

const translationCache = new Map()

export const translationService = {
  /**
   * Fetch localized messages from backend API
   * @param {string} locale - Language code (e.g., 'pt-BR', 'en-US')
   * @returns {Promise<Object>} Messages object
   */
  async getMessages(locale = null) {
    // Use cache if available
    const cacheKey = locale || 'default'
    if (translationCache.has(cacheKey)) {
      return translationCache.get(cacheKey)
    }

    try {
      const response = await api.get('/i18n/messages', {
        headers: locale ? { 'Accept-Language': locale } : {}
      })
      
      const messages = response.data.messages
      translationCache.set(cacheKey, messages)
      return messages
    } catch (error) {
      console.error('Failed to fetch localized messages:', error)
      return {}
    }
  },

  /**
   * Get all available locales
   * @returns {Promise<Array>} List of available locales
   */
  async getAvailableLocales() {
    try {
      const response = await api.get('/i18n/locales')
      return response.data.locales
    } catch (error) {
      console.error('Failed to fetch available locales:', error)
      return [
        { code: 'pt-BR', name: 'Português (BR)' },
        { code: 'en-US', name: 'English (US)' }
      ]
    }
  },

  /**
   * Set user's language preference on backend
   * @param {string} locale - Language code to set
   * @returns {Promise<Object>} Success response
   */
  async setLocale(locale) {
    try {
      const response = await api.post('/i18n/set-locale', { locale })
      // Clear cache when locale changes
      translationCache.clear()
      return response.data
    } catch (error) {
      console.error('Failed to set locale:', error)
      return { success: false, error: error.message }
    }
  },

  /**
   * Clear translation cache (useful when language changes)
   */
  clearCache() {
    translationCache.clear()
  }
}

export default translationService
