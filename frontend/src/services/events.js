import api from "./api";

export default {
  list() {
    return api.get("/events");
  },
  get(id) {
    return api.get(`/events/${id}`);
  },
  create(name, date, time) {
    return api.post("/events", { name, date, time });
  },
  updateStatus(id, active) {
    return api.patch(`/events/${id}/status`, { active });
  },
  delete(id) {
    return api.delete(`/events/${id}`);
  },
};
