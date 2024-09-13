import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Your FastAPI backend URL
});

export const getUsersByCity = (city) => api.get(`/users/city/${city}`);
