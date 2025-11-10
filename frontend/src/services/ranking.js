import api from './api';

export default {
  getRanking(eventId) {
    return api.get(`/ranking/${eventId}`);
  },

  getEventRanking(eventId) {
    return api.get(`/ranking/${eventId}`);
  },

  getLeaderboard(eventId) {
    return api.get(`/ranking?event_id=${eventId}`);
  },
};
