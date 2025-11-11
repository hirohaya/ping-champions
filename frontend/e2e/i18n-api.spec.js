import { test, expect } from '@playwright/test'

/**
 * E2E Tests for Backend i18n API
 * Tests communication between frontend and backend i18n endpoints
 */

test.describe('Backend i18n API Integration', () => {
  const API_BASE = 'http://127.0.0.1:8000/api/i18n'

  test.describe('API Endpoints', () => {
    test('should fetch available locales from backend', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/locales`)
      
      expect(response.ok()).toBeTruthy()
      
      const data = await response.json()
      expect(data).toHaveProperty('locales')
      expect(Array.isArray(data.locales)).toBeTruthy()
      expect(data.locales.length).toBeGreaterThan(0)
    })

    test('should return correct locale information', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/locales`)
      const data = await response.json()
      
      // Should have pt-BR
      const ptBR = data.locales.find(l => l.code === 'pt-BR')
      expect(ptBR).toBeTruthy()
      expect(ptBR.name).toBe('Português (BR)')
      
      // Should have en-US
      const enUS = data.locales.find(l => l.code === 'en-US')
      expect(enUS).toBeTruthy()
      expect(enUS.name).toBe('English (US)')
    })

    test('should fetch English messages by default', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`)
      
      expect(response.ok()).toBeTruthy()
      
      const data = await response.json()
      expect(data).toHaveProperty('locale')
      expect(data).toHaveProperty('messages')
      expect(typeof data.messages).toBe('object')
    })

    test('should fetch Portuguese messages with pt-BR header', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'pt-BR'
        }
      })
      
      expect(response.ok()).toBeTruthy()
      
      const data = await response.json()
      expect(data.locale).toBe('pt-BR')
      expect(data.messages).toBeTruthy()
    })

    test('should fetch English messages with en-US header', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'en-US'
        }
      })
      
      expect(response.ok()).toBeTruthy()
      
      const data = await response.json()
      expect(data.locale).toBe('en-US')
      expect(data.messages).toBeTruthy()
    })

    test('should allow setting locale preference', async ({ page }) => {
      const response = await page.request.post(`${API_BASE}/set-locale`, {
        data: {
          locale: 'pt-BR'
        }
      })
      
      expect(response.ok()).toBeTruthy()
      
      const data = await response.json()
      expect(data.success).toBe(true)
      expect(data.locale).toBe('pt-BR')
    })

    test('should reject invalid locale', async ({ page }) => {
      const response = await page.request.post(`${API_BASE}/set-locale`, {
        data: {
          locale: 'invalid-XX'
        }
      })
      
      const data = await response.json()
      expect(data.success).toBe(false)
      expect(data.error).toBeTruthy()
    })
  })

  test.describe('Message Content', () => {
    test('should contain common translation keys in English', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'en-US'
        }
      })
      
      const data = await response.json()
      const messages = data.messages
      
      // Check for common keys
      expect(messages).toHaveProperty('success')
      expect(messages).toHaveProperty('error')
      expect(messages).toHaveProperty('not_found')
      expect(messages.success).toBe('Success')
      expect(messages.error).toBe('Error')
    })

    test('should contain common translation keys in Portuguese', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'pt-BR'
        }
      })
      
      const data = await response.json()
      const messages = data.messages
      
      // Check for common keys
      expect(messages).toHaveProperty('success')
      expect(messages).toHaveProperty('error')
      expect(messages).toHaveProperty('not_found')
      expect(messages.success).toBe('Sucesso')
      expect(messages.error).toBe('Erro')
    })

    test('should contain event-related messages', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'en-US'
        }
      })
      
      const data = await response.json()
      const messages = data.messages
      
      expect(messages).toHaveProperty('event_created')
      expect(messages).toHaveProperty('event_updated')
      expect(messages).toHaveProperty('event_deleted')
      expect(messages.event_created).toContain('success')
    })

    test('should contain player-related messages', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'en-US'
        }
      })
      
      const data = await response.json()
      const messages = data.messages
      
      expect(messages).toHaveProperty('player_registered')
      expect(messages).toHaveProperty('player_updated')
      expect(messages).toHaveProperty('player_deleted')
    })

    test('should contain match-related messages', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'en-US'
        }
      })
      
      const data = await response.json()
      const messages = data.messages
      
      expect(messages).toHaveProperty('match_created')
      expect(messages).toHaveProperty('match_updated')
      expect(messages).toHaveProperty('match_deleted')
    })

    test('should have matching keys between languages', async ({ page }) => {
      const enResponse = await page.request.get(`${API_BASE}/messages`, {
        headers: { 'Accept-Language': 'en-US' }
      })
      const ptResponse = await page.request.get(`${API_BASE}/messages`, {
        headers: { 'Accept-Language': 'pt-BR' }
      })
      
      const enMessages = (await enResponse.json()).messages
      const ptMessages = (await ptResponse.json()).messages
      
      // Get keys from both
      const enKeys = Object.keys(enMessages).sort()
      const ptKeys = Object.keys(ptMessages).sort()
      
      // Should have same keys
      expect(enKeys).toEqual(ptKeys)
    })
  })

  test.describe('Accept-Language Header Handling', () => {
    test('should default to English when no Accept-Language header', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`)
      
      const data = await response.json()
      expect(data.locale).toBe('en-US')
    })

    test('should handle multiple Accept-Language preferences', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'fr-FR,fr;q=0.9,pt-BR;q=0.8,pt;q=0.7,en;q=0.6'
        }
      })
      
      const data = await response.json()
      // Should return Portuguese since it's in the list
      expect(['pt-BR', 'en-US']).toContain(data.locale)
    })

    test('should fallback to English for unsupported languages', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'ja-JP,ja;q=0.9'
        }
      })
      
      const data = await response.json()
      // Should fallback to English
      expect(data.locale).toBe('en-US')
    })

    test('should handle language code variants', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: {
          'Accept-Language': 'pt'
        }
      })
      
      const data = await response.json()
      // Should recognize 'pt' as Portuguese
      expect(data.locale).toBe('pt-BR')
    })
  })

  test.describe('Response Format', () => {
    test('should return valid JSON for locales endpoint', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/locales`)
      
      // Should be valid JSON
      let data
      try {
        data = await response.json()
        expect(data).toBeTruthy()
      } catch (e) {
        throw new Error('Invalid JSON response')
      }
    })

    test('should return messages as object not array', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`)
      const data = await response.json()
      
      expect(Array.isArray(data.messages)).toBe(false)
      expect(typeof data.messages).toBe('object')
    })

    test('should include locale in response', async ({ page }) => {
      const response = await page.request.get(`${API_BASE}/messages`, {
        headers: { 'Accept-Language': 'pt-BR' }
      })
      
      const data = await response.json()
      expect(data).toHaveProperty('locale')
      expect(data.locale).toBe('pt-BR')
    })

    test('set-locale response should indicate success', async ({ page }) => {
      const response = await page.request.post(`${API_BASE}/set-locale`, {
        data: { locale: 'pt-BR' }
      })
      
      const data = await response.json()
      expect(data).toHaveProperty('success')
      expect(data).toHaveProperty('locale')
    })
  })

  test.describe('HTTP Methods', () => {
    test('locales endpoint should only accept GET', async ({ page }) => {
      // POST should not work
      const postResponse = await page.request.post(`${API_BASE}/locales`)
      expect(postResponse.status()).toBe(405) // Method Not Allowed
    })

    test('messages endpoint should only accept GET', async ({ page }) => {
      const postResponse = await page.request.post(`${API_BASE}/messages`)
      expect(postResponse.status()).toBe(405)
    })

    test('set-locale endpoint should only accept POST', async ({ page }) => {
      const getResponse = await page.request.get(`${API_BASE}/set-locale`)
      expect(getResponse.status()).toBe(405)
    })
  })
})
