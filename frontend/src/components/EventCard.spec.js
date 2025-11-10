import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import EventCard from '@/components/EventCard.vue'

describe('EventCard.vue', () => {
  const mockEvent = {
    id: 1,
    name: 'Spring Tournament',
    date: '2025-05-15',
    time: '14:00',
  }

  const createWrapper = (event = mockEvent) => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [
        {
          path: '/events/:id',
          name: 'EventDetail',
          component: { template: '<div>Event Detail</div>' },
        },
      ],
    })

    return mount(EventCard, {
      props: {
        event,
      },
      global: {
        plugins: [router],
      },
    })
  }

  it('renders event name', () => {
    const wrapper = createWrapper()
    expect(wrapper.text()).toContain('Spring Tournament')
  })

  it('renders event date and time', () => {
    const wrapper = createWrapper()
    expect(wrapper.text()).toContain('2025-05-15')
    expect(wrapper.text()).toContain('14:00')
  })

  it('renders event card container', () => {
    const wrapper = createWrapper()
    expect(wrapper.find('.evento-card').exists()).toBe(true)
  })

  it('has delete button', () => {
    const wrapper = createWrapper()
    expect(wrapper.find('.excluir-btn').exists()).toBe(true)
  })

  it('emits delete-event when delete button clicked', async () => {
    const wrapper = createWrapper()
    await wrapper.find('.excluir-btn').trigger('click')
    expect(wrapper.emitted()).toHaveProperty('delete-event')
    expect(wrapper.emitted('delete-event')[0]).toEqual([1])
  })

  it('handles missing optional fields gracefully', () => {
    const minimalEvent = {
      id: 1,
      name: 'Event',
    }
    const wrapper = createWrapper(minimalEvent)
    expect(wrapper.text()).toContain('Event')
  })

  it('navigates to event detail on card click', async () => {
    const router = createRouter({
      history: createMemoryHistory(),
      routes: [
        {
          path: '/events/:id',
          name: 'EventDetail',
          component: { template: '<div>Event Detail</div>' },
        },
      ],
    })

    const pushSpy = vi.spyOn(router, 'push')
    const wrapper = mount(EventCard, {
      props: { event: mockEvent },
      global: { plugins: [router] },
    })

    await wrapper.find('.evento-card').trigger('click')
    expect(pushSpy).toHaveBeenCalledWith('/events/1')
  })
})
