import axios from 'axios';
import { API_BASE_URL, POC_PREFIX } from '../config';

const api = axios.create({
  baseURL: `${API_BASE_URL}${POC_PREFIX}`
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Task API functions
export const getTasks = () => api.get('/tasks');
export const getTask = (id: number) => api.get(`/tasks/${id}`);
export const createTask = (data: any) => api.post('/tasks', data);
export const updateTask = (id: number, data: any) => api.put(`/tasks/${id}`, data);
export const deleteTask = (id: number) => api.delete(`/tasks/${id}`);
