/**
 * i18n Router Guard
 * 
 * Automatically loads translations when navigating to routes
 * Prevents flickering by ensuring translations are loaded before component renders
 */

import localeLoader from '@/utils/localeLoader'
import { useI18n } from 'vue-i18n'

/**
 * Create router guard for i18n lazy loading
 * Usage in router setup:
 *   import { createI18nGuard } from '@/router/i18nGuard'
 *   router.beforeEach(createI18nGuard())
 */
export function createI18nGuard() {
  return async (to, from, next) => {
    const { locale } = useI18n()
    
    // Map route names to namespace groups
    const routeNamespaceMap = {
      'Events': ['events'],
      'EventDetail': ['events', 'players', 'matches', 'ranking'],
      'Players': ['players'],
      'Matches': ['matches'],
      'Ranking': ['ranking'],
      'Home': ['navigation'],
      'Status': ['messages']
    }
    
    const namespaces = routeNamespaceMap[to.name] || []
    
    // Preload translations for the target route
    if (namespaces.length > 0) {
      try {
        await localeLoader.loadNamespaces(locale.value, namespaces)
      } catch (err) {
        console.error('Failed to preload translations:', err)
        // Continue anyway, fallback to cached or default
      }
    }
    
    next()
  }
}

/**
 * Hook to manually load translations for a route
 * Usage in component:
 *   import { useLoadTranslations } from '@/router/i18nGuard'
 *   onMounted(() => useLoadTranslations('events', 'players'))
 */
export function useLoadTranslations(...namespaces) {
  const { locale } = useI18n()
  
  return Promise.all(
    namespaces.map(ns => localeLoader.loadNamespace(locale.value, ns))
  )
}

export default createI18nGuard
