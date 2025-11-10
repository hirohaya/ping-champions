import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // ajuste conforme necessário
});

export default api;
