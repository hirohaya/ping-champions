import api from "./api";

export default {
  list(event_id) {
    return api.get("/players", { params: { event_id } });
  },
  create(name, event_id) {
    return api.post("/players", { name, event_id });
  },
  update(player_id, name) {
    return api.put(`/players/${player_id}`, { name });
  },
  delete(player_id) {
    return api.delete(`/players/${player_id}`);
  },
  listAll() {
    return api.get("/players/all");
  },
};
