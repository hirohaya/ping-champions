import api from './api'

export default {
  list() {
    return api.get('/events')
  },
  create(name, date, time) {
    return api.post('/events/create', { name, date, time })
  },
  delete(id) {
    return api.post(`/events/delete/${id}`)
  }
}
