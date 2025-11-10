import { describe, it, expect, beforeEach } from 'vitest'
import api from '@/services/api'

describe('API Service', () => {
  it('creates axios instance with correct base URL', () => {
    expect(api).toBeDefined()
    expect(api.defaults.baseURL).toBe('http://localhost:8000')
  })

  it('has default headers configured', () => {
    expect(api.defaults.headers.common).toBeDefined()
  })

  it('supports GET requests', () => {
    expect(api.get).toBeDefined()
    expect(typeof api.get).toBe('function')
  })

  it('supports POST requests', () => {
    expect(api.post).toBeDefined()
    expect(typeof api.post).toBe('function')
  })

  it('supports PUT requests', () => {
    expect(api.put).toBeDefined()
    expect(typeof api.put).toBe('function')
  })

  it('supports DELETE requests', () => {
    expect(api.delete).toBeDefined()
    expect(typeof api.delete).toBe('function')
  })

  it('has timeout configured', () => {
    expect(api.defaults.timeout).toBeDefined()
    expect(typeof api.defaults.timeout).toBe('number')
  })
})
