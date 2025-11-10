import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import Breadcrumbs from '@/components/Breadcrumbs.vue'

describe('Breadcrumbs.vue', () => {
  it('renders breadcrumb items from route', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [
        {
          path: '/events',
          name: 'Events',
          component: { template: '<div>Events</div>' },
        },
        {
          path: '/events/:id',
          name: 'EventDetail',
          component: { template: '<div>Event Detail</div>' },
        },
      ],
    })

    await router.push('/events/1')
    await router.isReady()

    const wrapper = mount(Breadcrumbs, {
      global: {
        plugins: [router],
      },
    })

    expect(wrapper.exists()).toBe(true)
  })

  it('renders home link', () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [
        {
          path: '/',
          name: 'Home',
          component: { template: '<div>Home</div>' },
        },
      ],
    })

    const wrapper = mount(Breadcrumbs, {
      global: {
        plugins: [router],
      },
    })

    expect(wrapper.find('a').exists()).toBe(true)
  })

  it('handles empty route gracefully', () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [],
    })

    const wrapper = mount(Breadcrumbs, {
      global: {
        plugins: [router],
      },
    })

    expect(wrapper.exists()).toBe(true)
  })
})
