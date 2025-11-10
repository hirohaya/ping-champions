import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for E2E testing
 * Tests run against both backend (http://127.0.0.1:8000) and frontend (http://localhost:5173)
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: false, // Run tests sequentially to avoid database state issues
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : 1,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],

  webServer: [
    {
      command: 'npm run dev',
      port: 5173,
      timeout: 120 * 1000,
      reuseExistingServer: !process.env.CI,
    },
    {
      command: 'python run_backend.py',
      port: 8000,
      timeout: 120 * 1000,
      reuseExistingServer: !process.env.CI,
      cwd: '..',
    },
  ],
});
