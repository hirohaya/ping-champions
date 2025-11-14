import axios from "axios";

// Usar variável de ambiente se disponível, caso contrário usar localhost
const baseURL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: baseURL,
});

export default api;
