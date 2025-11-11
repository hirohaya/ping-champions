/**
 * Locale Loader - Route-based Translation Loader
 * 
 * Loads translations on-demand per route for optimal performance
 * Caches loaded translations to avoid repeated requests
 */

class LocaleLoader {
  constructor() {
    this.cache = {}
    this.loading = {}
  }

  /**
   * Load namespace for a specific locale
   * @param {string} locale - Locale code (e.g., 'pt-BR')
   * @param {string} namespace - Namespace to load (e.g., 'events')
   * @returns {Promise<Object>} Namespace messages
   */
  async loadNamespace(locale, namespace) {
    const cacheKey = `${locale}:${namespace}`
    
    // Return from cache if available
    if (this.cache[cacheKey]) {
      return this.cache[cacheKey]
    }
    
    // Return promise if already loading
    if (this.loading[cacheKey]) {
      return this.loading[cacheKey]
    }
    
    // Load from file
    const loadPromise = (async () => {
      try {
        const module = await import(`./locales/${locale}/${namespace}.json`)
        const messages = module.default
        this.cache[cacheKey] = messages
        return messages
      } catch (err) {
        console.error(`Failed to load ${namespace} for ${locale}:`, err)
        return {}
      } finally {
        delete this.loading[cacheKey]
      }
    })()
    
    this.loading[cacheKey] = loadPromise
    return loadPromise
  }

  /**
   * Load multiple namespaces for a locale
   * @param {string} locale - Locale code
   * @param {Array<string>} namespaces - Namespace names
   * @returns {Promise<Object>} All namespaces merged
   */
  async loadNamespaces(locale, namespaces) {
    const promises = namespaces.map(ns => this.loadNamespace(locale, ns))
    const results = await Promise.all(promises)
    
    const merged = {}
    namespaces.forEach((ns, idx) => {
      merged[ns] = results[idx]
    })
    
    return merged
  }

  /**
   * Preload common namespaces (called on app init)
   * @param {string} locale - Locale code
   * @returns {Promise<void>}
   */
  async preloadCommon(locale) {
    const commonNamespaces = ['common', 'navigation', 'messages']
    await this.loadNamespaces(locale, commonNamespaces)
  }

  /**
   * Load namespaces for a specific feature/route
   * Common routes and their required namespaces:
   * - /events -> events
   * - /players/:id -> players
   * - /matches/:id -> matches
   * - /ranking/:id -> ranking
   * 
   * @param {string} locale - Locale code
   * @param {string} route - Route name or path
   * @returns {Promise<void>}
   */
  async preloadForRoute(locale, route) {
    const routeNamespaces = {
      'events': ['events'],
      'players': ['players'],
      'matches': ['matches'],
      'ranking': ['ranking'],
      'event-detail': ['events', 'players', 'matches', 'ranking'],
      'default': [] // No specific namespaces
    }
    
    const namespaces = routeNamespaces[route] || routeNamespaces['default']
    if (namespaces.length > 0) {
      await this.loadNamespaces(locale, namespaces)
    }
  }

  /**
   * Clear cache for a specific locale or all locales
   * @param {string|null} locale - Locale to clear, or null for all
   */
  clearCache(locale = null) {
    if (locale) {
      // Clear specific locale
      Object.keys(this.cache).forEach(key => {
        if (key.startsWith(locale)) {
          delete this.cache[key]
        }
      })
    } else {
      // Clear all
      this.cache = {}
      this.loading = {}
    }
  }

  /**
   * Get cache statistics (useful for debugging)
   * @returns {Object} Cache stats
   */
  getStats() {
    const entries = Object.keys(this.cache).length
    const size = JSON.stringify(this.cache).length
    return {
      entries,
      sizeBytes: size,
      sizeKB: (size / 1024).toFixed(2)
    }
  }
}

// Create singleton instance
const localeLoader = new LocaleLoader()

export default localeLoader
