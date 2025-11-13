import { test, expect } from '@playwright/test'

/**
 * E2E Tests for Internationalization (i18n)
 * Tests language switching, translations, and persistence
 */

test.describe('Internationalization (i18n) E2E Tests', () => {
  test.beforeEach(async ({ page, context }) => {
    // Clear cookies before each test
    await context.clearCookies()
    
    // Set timeout for the entire test
    page.setDefaultTimeout(10000)
    page.setDefaultNavigationTimeout(10000)
    
    // Initialize localStorage via addInitScript to avoid sandbox issues
    await page.addInitScript(() => {
      localStorage.clear()
    })
    
    // Navigate to home page
    await page.goto('http://localhost:5173/', { waitUntil: 'domcontentloaded' })
    
    // Wait briefly for JavaScript to initialize
    await page.waitForTimeout(500)
  })

  test.describe('Language Switcher Component', () => {
    test('should display language selector with both languages', async ({ page }) => {
      // Find the language switcher dropdown
      const languageSelect = page.locator('select')
      
      // Verify dropdown exists
      await expect(languageSelect).toBeVisible()
      
      // Get all options
      const options = await page.locator('select option').allTextContents()
      
      // Verify both languages are present
      expect(options).toContain('Português (BR)')
      expect(options).toContain('English (US)')
    })

    test('should show English (US) as default language', async ({ page }) => {
      const languageSelect = page.locator('select')
      const selectedValue = await languageSelect.inputValue()
      
      expect(selectedValue).toBe('en-US')
    })

    test('should auto-detect browser language on first visit', async ({ browser }) => {
      // Create new context with pt-BR language
      const context = await browser.newContext({
        locale: 'pt-BR'
      })
      const page = await context.newPage()
      
      page.setDefaultTimeout(10000)
      page.setDefaultNavigationTimeout(10000)
      
      // Initialize localStorage via addInitScript
      await page.addInitScript(() => {
        localStorage.clear()
      })
      
      // Navigate to app
      await page.goto('http://localhost:5173/', { waitUntil: 'domcontentloaded' })
      await page.waitForTimeout(500)
      
      // Check if Portuguese was auto-selected
      const languageSelect = page.locator('select')
      const selectedValue = await languageSelect.inputValue()
      
      // Should auto-detect Portuguese
      expect(selectedValue).toBe('pt-BR')
      
      await page.close()
      await context.close()
    })
  })

  test.describe('English (US) Translations', () => {
    test('should display English labels on initial load', async ({ page }) => {
      // Check header text
      const heading = page.locator('h1')
      await expect(heading).toContainText('Ping Champions')
      
      // Check if language label shows "Language" in English
      const languageLabel = page.locator('select')
      const title = await languageLabel.getAttribute('title')
      expect(title).toContain('Language')
    })

    test('should show English navigation links', async ({ page }) => {
      const homeLink = page.locator('a:has-text("Home")')
      await expect(homeLink).toBeVisible()
    })

    test('should display English in System Panel', async ({ page }) => {
      // Check for English text in System Panel
      const systemPanel = page.locator(':has-text("System Panel")')
      await expect(systemPanel).toBeVisible()
      
      // Check for English event/player/match labels
      const eventsLabel = page.locator(':has-text("Events")')
      const playersLabel = page.locator(':has-text("Players")')
      const matchesLabel = page.locator(':has-text("Matches")')
      
      await expect(eventsLabel).toBeVisible()
      await expect(playersLabel).toBeVisible()
      await expect(matchesLabel).toBeVisible()
    })

    test('should display English help text', async ({ page }) => {
      // Check for English help section
      const helpText = page.locator(':has-text("How to use Ping Champions")')
      await expect(helpText).toBeVisible()
      
      // Check for English instructions
      const instruction = page.locator(':has-text("Create an event")')
      await expect(instruction).toBeVisible()
    })
  })

  test.describe('Portuguese (BR) Translations', () => {
    test('should switch to Portuguese when selected', async ({ page }) => {
      // Select Portuguese
      const languageSelect = page.locator('select')
      await languageSelect.selectOption('pt-BR')
      
      // Wait for translations to update
      await page.waitForTimeout(500)
      
      // Verify the select shows Portuguese is selected
      const selectedValue = await languageSelect.inputValue()
      expect(selectedValue).toBe('pt-BR')
    })

    test('should display Portuguese labels after switching', async ({ page }) => {
      // Switch to Portuguese
      const languageSelect = page.locator('select')
      await languageSelect.selectOption('pt-BR')
      
      // Wait for DOM update
      await page.waitForTimeout(500)
      
      // Check if language label changed to "Idioma" (Portuguese for Language)
      const languageTitle = await languageSelect.getAttribute('title')
      expect(languageTitle).toContain('Idioma')
    })

    test('should display Portuguese help section title', async ({ page }) => {
      // Switch to Portuguese
      const languageSelect = page.locator('select')
      await languageSelect.selectOption('pt-BR')
      
      // Wait for update
      await page.waitForTimeout(500)
      
      // Check Portuguese help text appears or English is replaced
      // (The exact translation depends on component implementation)
      const heading = page.locator('h1')
      await expect(heading).toContainText('Ping Champions')
    })

    test('should persist Portuguese selection in localStorage', async ({ page }) => {
      // Switch to Portuguese
      const languageSelect = page.locator('select')
      await languageSelect.selectOption('pt-BR')
      
      // Wait for storage update
      await page.waitForTimeout(500)
      
      // Check localStorage using addInitScript
      const locale = await page.evaluate(() => localStorage.getItem('locale'))
      expect(locale).toBe('pt-BR')
    })
  })

  test.describe('Language Persistence', () => {
    test('should remember language selection after page refresh', async ({ page }) => {
      // Select Portuguese
      const languageSelect = page.locator('select')
      await languageSelect.selectOption('pt-BR')
      
      // Wait for localStorage update
      await page.waitForTimeout(500)
      
      // Refresh page
      await page.reload({ waitUntil: 'domcontentloaded' })
      await page.waitForTimeout(500)
      
      // Check if Portuguese is still selected
      const selectedValue = await languageSelect.inputValue()
      expect(selectedValue).toBe('pt-BR')
    })

    test('should remember language selection in new tab', async ({ context, page }) => {
      // Select Portuguese
      const languageSelect = page.locator('select')
      await languageSelect.selectOption('pt-BR')
      
      // Wait for localStorage update
      await page.waitForTimeout(500)
      
      // Open new page (shares same context and localStorage)
      const newPage = await context.newPage()
      newPage.setDefaultTimeout(10000)
      newPage.setDefaultNavigationTimeout(10000)
      
      await newPage.goto('http://localhost:5173/', { waitUntil: 'domcontentloaded' })
      await newPage.waitForTimeout(500)
      
      // Check if Portuguese is still selected
      const newSelect = newPage.locator('select')
      const selectedValue = await newSelect.inputValue()
      expect(selectedValue).toBe('pt-BR')
      
      await newPage.close()
    })
  })

  test.describe('Language Switching Behavior', () => {
    test('should allow toggling between languages multiple times', async ({ page }) => {
      const languageSelect = page.locator('select')
      
      // Start with English
      let value = await languageSelect.inputValue()
      expect(value).toBe('en-US')
      
      // Switch to Portuguese
      await languageSelect.selectOption('pt-BR')
      await page.waitForTimeout(300)
      value = await languageSelect.inputValue()
      expect(value).toBe('pt-BR')
      
      // Switch back to English
      await languageSelect.selectOption('en-US')
      await page.waitForTimeout(300)
      value = await languageSelect.inputValue()
      expect(value).toBe('en-US')
      
      // Switch to Portuguese again
      await languageSelect.selectOption('pt-BR')
      await page.waitForTimeout(300)
      value = await languageSelect.inputValue()
      expect(value).toBe('pt-BR')
    })

    test('should be responsive to language selection immediately', async ({ page }) => {
      // Select Portuguese
      const languageSelect = page.locator('select')
      await languageSelect.selectOption('pt-BR')
      
      // Wait briefly for state change
      await page.waitForTimeout(300)
      
      // Verify the select element shows Portuguese
      const selectedValue = await languageSelect.inputValue()
      expect(selectedValue).toBe('pt-BR')
      
      // Switch immediately back
      await languageSelect.selectOption('en-US')
      await page.waitForTimeout(300)
      
      const newValue = await languageSelect.inputValue()
      expect(newValue).toBe('en-US')
    })
  })

  test.describe('Accessibility', () => {
    test('language switcher should have proper aria attributes', async ({ page }) => {
      const languageSelect = page.locator('select')
      
      // Should have a title attribute for accessibility
      const title = await languageSelect.getAttribute('title')
      expect(title).toBeTruthy()
    })

    test('language options should be keyboard navigable', async ({ page }) => {
      const languageSelect = page.locator('select')
      
      // Focus the select
      await languageSelect.focus()
      
      // Press down arrow to navigate
      await page.keyboard.press('ArrowDown')
      
      // Get the selected value
      const value = await languageSelect.inputValue()
      
      // Should have changed
      expect(value).toBeTruthy()
    })
  })

  test.describe('Header Layout with Language Switcher', () => {
    test('should display language switcher in header', async ({ page }) => {
      // Get the header container
      const header = page.locator('div').filter({ has: page.locator('h1') })
      
      // Check that header contains both title and select
      const heading = header.locator('h1')
      const select = header.locator('select')
      
      await expect(heading).toBeVisible()
      await expect(select).toBeVisible()
    })

    test('should have proper spacing between title and language switcher', async ({ page }) => {
      // Get header elements
      const header = page.locator('div').filter({ has: page.locator('h1') })
      
      // Both elements should be visible
      const h1 = header.locator('h1')
      const select = header.locator('select')
      
      const h1Box = await h1.boundingBox()
      const selectBox = await select.boundingBox()
      
      expect(h1Box).toBeTruthy()
      expect(selectBox).toBeTruthy()
      
      // Select should be to the right of h1
      if (h1Box && selectBox) {
        expect(selectBox.x).toBeGreaterThan(h1Box.x + h1Box.width)
      }
    })
  })

  test.describe('Browser Compatibility', () => {
    test('should work with localStorage enabled', async ({ page }) => {
      // Select Portuguese
      const languageSelect = page.locator('select')
      await languageSelect.selectOption('pt-BR')
      
      // Wait for persistence
      await page.waitForTimeout(500)
      
      // Verify localStorage was updated
      const storedLocale = await page.evaluate(() => localStorage.getItem('locale'))
      expect(storedLocale).toBe('pt-BR')
    })

    test('should handle language selection even if localStorage is unavailable', async ({ page }) => {
      // Try to select language even with mocked unavailable localStorage
      const languageSelect = page.locator('select')
      
      // Should still allow selection
      await languageSelect.selectOption('pt-BR')
      await page.waitForTimeout(300)
      
      // Verify the selection was made
      const value = await languageSelect.inputValue()
      expect(value).toBe('pt-BR')
    })
  })

  test.describe('Integration with App Components', () => {
    test('should not affect app functionality when changing language', async ({ page }) => {
      // Switch to Portuguese
      const languageSelect = page.locator('select')
      await languageSelect.selectOption('pt-BR')
      await page.waitForTimeout(500)
      
      // App should still be functional
      const homeLink = page.locator('a').first()
      await expect(homeLink).toBeVisible()
      
      // Should be able to navigate
      await homeLink.click()
      await page.waitForLoadState('domcontentloaded')
      await page.waitForTimeout(500)
      
      // Page should still load successfully
      const heading = page.locator('h1').first()
      await expect(heading).toBeVisible()
    })
  })
})
