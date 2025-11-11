import api from "./api";

export default {
  create(data) {
    return api.post("/matches", data);
  },
  getEventMatches(event_id) {
    return api.get("/matches", { params: { event_id } });
  },
  listarPorEvento(event_id) {
    return api.get("/matches", { params: { event_id } });
  },
  listarTodos() {
    return api.get("/matches/all/list");
  },
  get(id) {
    return api.get(`/matches/${id}`);
  },
  update(id, data) {
    return api.put(`/matches/${id}`, data);
  },
  delete(id) {
    return api.delete(`/matches/${id}`);
  },
};
