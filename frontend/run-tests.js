#!/usr/bin/env node

/**
 * Simple test runner that manages backend/frontend servers and runs Playwright tests
 * This avoids hanging issues with server startup in Playwright config
 */

import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const BACKEND_PORT = 8000;
const FRONTEND_PORT = 5174;
const BACKEND_URL = `http://127.0.0.1:${BACKEND_PORT}`;
const FRONTEND_URL = `http://localhost:${FRONTEND_PORT}`;
const TIMEOUT = 30000; // 30 seconds to start servers

let backendProcess = null;
let frontendProcess = null;

/**
 * Wait for a service to be available
 */
async function waitForService(url, timeout = 10000) {
  const startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    try {
      const response = await fetch(url, { signal: AbortSignal.timeout(2000) });
      if (response.ok || response.status < 500) {
        console.log(`✓ Service ready: ${url}`);
        return true;
      }
    } catch (err) {
      // Service not ready yet
    }
    await new Promise(resolve => setTimeout(resolve, 500));
  }
  throw new Error(`Service not ready after ${timeout}ms: ${url}`);
}

/**
 * Start backend server
 */
function startBackend() {
  return new Promise((resolve, reject) => {
    console.log('Starting backend...');
    const backendPath = path.join(__dirname, '..', 'run_backend.py');
    
    backendProcess = spawn('python', [backendPath], {
      stdio: ['ignore', 'pipe', 'pipe'],
      cwd: path.join(__dirname, '..'),
    });

    let started = false;
    const timeout = setTimeout(() => {
      if (!started) {
        reject(new Error('Backend startup timeout'));
      }
    }, TIMEOUT);

    const checkReady = async () => {
      try {
        await waitForService(BACKEND_URL, 5000);
        started = true;
        clearTimeout(timeout);
        resolve();
      } catch (err) {
        // Keep waiting
      }
    };

    backendProcess.stderr.on('data', (data) => {
      const output = data.toString();
      if (output.includes('Uvicorn running on')) {
        checkReady();
      }
    });

    backendProcess.on('error', reject);
    backendProcess.on('exit', (code) => {
      if (!started && code !== 0) {
        reject(new Error(`Backend exited with code ${code}`));
      }
    });

    // Check periodically
    const interval = setInterval(checkReady, 2000);
    backendProcess.once('exit', () => clearInterval(interval));
  });
}

/**
 * Start frontend server
 */
function startFrontend() {
  return new Promise((resolve, reject) => {
    console.log('Starting frontend...');
    
    // Use npm.cmd on Windows, npm on Unix
    const npmCmd = process.platform === 'win32' ? 'npm.cmd' : 'npm';
    
    frontendProcess = spawn(npmCmd, ['run', 'dev'], {
      stdio: ['ignore', 'pipe', 'pipe'],
      cwd: __dirname,
      env: { ...process.env, VITE_PORT: FRONTEND_PORT },
      shell: true,
    });

    let started = false;
    const timeout = setTimeout(() => {
      if (!started) {
        reject(new Error('Frontend startup timeout'));
      }
    }, TIMEOUT);

    const checkReady = async () => {
      try {
        await waitForService(FRONTEND_URL, 5000);
        started = true;
        clearTimeout(timeout);
        resolve();
      } catch (err) {
        // Keep waiting
      }
    };

    frontendProcess.stdout.on('data', (data) => {
      const output = data.toString();
      if (output.includes('ready in') || output.includes('Local:')) {
        checkReady();
      }
    });

    frontendProcess.stderr.on('data', (data) => {
      const output = data.toString();
      console.error(`[Frontend] ${output}`);
    });

    frontendProcess.on('error', reject);
    frontendProcess.on('exit', (code) => {
      if (!started && code !== 0) {
        reject(new Error(`Frontend exited with code ${code}`));
      }
    });

    // Check periodically
    const interval = setInterval(checkReady, 2000);
    frontendProcess.once('exit', () => clearInterval(interval));
  });
}

/**
 * Run Playwright tests
 */
function runTests() {
  return new Promise((resolve, reject) => {
    console.log('Starting Playwright tests...');
    
    // Use npx.cmd on Windows, npx on Unix
    const npxCmd = process.platform === 'win32' ? 'npx.cmd' : 'npx';
    
    const testProcess = spawn(npxCmd, ['playwright', 'test', '--workers=1'], {
      stdio: 'inherit',
      cwd: __dirname,
      env: { ...process.env, SKIP_SERVER: '1' },
      shell: true,
    });

    testProcess.on('error', reject);
    testProcess.on('exit', (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`Tests failed with code ${code}`));
      }
    });
  });
}

/**
 * Cleanup processes
 */
function cleanup() {
  console.log('Cleaning up...');
  if (backendProcess) {
    backendProcess.kill('SIGTERM');
  }
  if (frontendProcess) {
    frontendProcess.kill('SIGTERM');
  }
}

/**
 * Main
 */
async function main() {
  try {
    await startBackend();
    console.log('✓ Backend started');
    
    await startFrontend();
    console.log('✓ Frontend started');
    
    await runTests();
    console.log('✓ Tests completed');
    
    cleanup();
    process.exit(0);
  } catch (err) {
    console.error('ERROR:', err.message);
    cleanup();
    process.exit(1);
  }
}

// Handle signals
process.on('SIGINT', () => {
  console.log('\nInterrupted');
  cleanup();
  process.exit(1);
});

process.on('SIGTERM', () => {
  cleanup();
  process.exit(1);
});

main();
